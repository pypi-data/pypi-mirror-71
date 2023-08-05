import concurrent.futures
from copy import deepcopy
from dataclasses import asdict
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import Union, Sequence, Mapping

import pyqalx
from OrcFxAPI import Model
from pyqalx import QalxSession, Item

from qalx_orcaflex import data_models
from qalx_orcaflex.helpers import (
    data_file_paths,
    required_results_from_yaml,
    clean_set_key,
)

LOAD_CASE_INFO = data_models.LoadCaseInfo()

ORCA_FLEX_JOB_OPTIONS = data_models.OrcaFlexJobOptions()


class QalxOrcaFlexError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class BaseSource:
    """base class for batch sources.

    Any child class must implement a `to_jobs` method which takes a base_job argument
    and returns a generator of jobs

    """

    def __init__(self, *args, **kwargs):
        pass

    def _update_copy(self, base, update):
        new = deepcopy(base)
        new.update(update)
        return new

    def _path_meta(self, data_file: Mapping, path: PathLike) -> Path:
        dfp = Path(path)
        data_file["meta"]["_class"] = "orcaflex.job.data_file"
        data_file["meta"]["data_file_path"] = str(dfp)
        data_file["meta"]["data_file_name"] = dfp.name
        data_file["meta"]["data_file_drive"] = dfp.drive
        data_file["meta"]["data_file_uri"] = dfp.as_uri()
        return dfp

    def to_jobs(self, base_job: Mapping) -> Mapping:
        raise NotImplementedError(
            "This method needs to be defined in all BaseSource child classes"
        )


class DataFileItemsSource(BaseSource):
    def __init__(self, items: Sequence[Item]):
        """an iterable of existing data file items.

        This is useful when re-running a batch with some updated info or settings.

        :param items:
        """
        super(DataFileItemsSource, self).__init__(items)
        self.items = items

    def to_jobs(self, base_job: Mapping) -> Mapping:
        for dfi in self.items:
            job = self._update_copy(
                base_job,
                {
                    "data_file": dfi,
                    "case_name": dfi["meta"]["data_file_name"].split(".")[0],
                },
            )
            yield job


class ModelSource(BaseSource):
    def __init__(self, model: Model, name: str):
        """an OrcFxAPI.Model instance as the source, requires a model name

        :param model: an OrcFxAPI.Model instance that you want to add to the batch
        :param name: the name of the model, used as the file name to save back later.
        """
        super(ModelSource, self).__init__(model, name)
        self.model_byes = model.SaveDataMem()
        self.name = name
        self._clean_name = clean_set_key(name)

    def to_jobs(self, base_job: Mapping) -> Mapping:
        data_file = {
            "input_file": BytesIO(self.model_byes),
            "meta": {
                "_class": "orcaflex.job.data_file",
                "data_file_name": f"{self.name}.dat",
            },
            "file_name": f"{self.name}.dat",
        }
        job = self._update_copy(
            base_job, {"data_file": data_file, "case_name": self._clean_name}
        )
        yield job


class FileSource(BaseSource):
    def __init__(self, path: PathLike):
        """a file source

        :param path:
        """
        super(FileSource, self).__init__(path)
        self.path = path

    def to_jobs(self, base_job: Mapping) -> Mapping:
        data_file = {"input_file": self.path, "meta": {}}
        dfp = self._path_meta(data_file, self.path)
        job = self._update_copy(
            base_job, {"data_file": data_file, "case_name": dfp.stem}
        )
        yield job


class DirectorySource(BaseSource):
    def __init__(
        self,
        directory: Union[PathLike, Sequence[PathLike]],
        include_yaml: bool = False,
        skip_fails: bool = False,
        recursive: bool = False,
    ):
        """takes a directory of files and adds them all.

        :param directory: path to search for data files
        :param include_yaml: include yml and yaml files (default=False)
        :param skip_fails: don't error if there is a failed path e.g. it is deleted while searching (default=False)
        :param recursive: search all subdirectories (default=False)
        """
        super(DirectorySource, self).__init__(
            directory, include_yaml, skip_fails, recursive
        )
        self.directory = directory
        self.include_yaml = include_yaml
        self.skip_fails = skip_fails
        self.recursive = recursive

    def to_jobs(self, base_job: Mapping) -> Mapping:
        for dfp in data_file_paths(
            self.directory, self.include_yaml, self.skip_fails, self.recursive
        ):
            data_file = {
                "input_file": str(dfp),
                "meta": {"_class": "orcaflex.job.data_file"},
            }
            self._path_meta(data_file, dfp)
            job = self._update_copy(
                base_job, {"data_file": data_file, "case_name": dfp.stem}
            )
            yield job


class OrcaFlexBatchManager:
    """manager class for collecting batch info"""

    def __init__(self):
        """instance is returned by :ref:OrcaFlexBatch as context manager

        This collects all the sources for the jobs added to the batch.
        """
        self.orcaflex_jobs = []

    def add(
        self,
        source: BaseSource,
        job_options: data_models.OrcaFlexJobOptions = ORCA_FLEX_JOB_OPTIONS,
        required_results: Union[
            PathLike, Sequence[Union[data_models.TimeHistory, data_models.RangeGraph]],
        ] = (),
        model_views: Sequence[data_models.ModelView] = (),
        load_case_info: data_models.LoadCaseInfo = LOAD_CASE_INFO,
    ):
        """add data files to a batch based on a source and extra options.

        :param source: a child of :ref:BaseSource that implements `to_jobs`
        :param job_options: various options and settings see
            :ref:data_models.OrcaFlexJobOptions
        :param required_results: an iterator containing :ref:data_models.TimeHistory
            or :ref:data_models.RangeGraph
            (a mix of both is allowed) or a path to a yaml file with the correct
            Results structure.
        :param model_views: an iterator containing :ref:data_models.ModelView
        :param load_case_info: information about the load case to be used during
            presentation of results
            see :ref:data_models.LoadCaseInfo
        :return: None
        """
        if isinstance(required_results, PathLike):
            required_results = required_results_from_yaml(required_results)
        base_job = {
            "job_options": job_options,
            "required_results": required_results,
            "load_case_info": load_case_info,
            "model_views": model_views,
        }
        for job in source.to_jobs(base_job):
            self.orcaflex_jobs.append(job)


class OrcaFlexBatch:
    """
    .. _OrcaFlexBatch:
    .. auto

    """

    def __init__(
        self,
        name,
        session: QalxSession,
        batch_options: data_models.BatchOptions,
        dry_run: bool = False,
        meta: Mapping = None,
        verbose: bool = False,
    ):
        """a batch of OrcaFlex data files

        :param name: name of the batch
        :param session: a QalxSession
        :param batch_options: see :ref:data_models.BatchOptions
        :param dry_run: if True will not build or submit the batch but will print name
            of each case
        :param meta: additional metadata to add to the group entitiy
        :param verbose: print statements of progress as build is in progress
        """
        self.name = name
        self.session = session
        self.batch_options = batch_options
        if self.batch_options.summarise_results and (
            not self.batch_options.wait_to_complete
        ):
            raise QalxOrcaFlexError(
                "summarise results must be set with the wait_to_complete option."
            )
        self.dry_run = dry_run
        standard_meta = {
            "_class": "orcaflex.batch",
            "name": self.name,
            "options": self.batch_options.__dict__,
            "state": "new",
        }
        if meta is None:
            self.meta = standard_meta
        else:
            self.meta = standard_meta
            self.meta.update(meta)
        self.verbose = verbose

    def _add_case(self, case_n: int, job: Mapping) -> str:
        """adds a case to qalx

        :param case_n: case number
        :param job: job data
        :return: str of the case_name
        """
        case_name = f"[{case_n + 1}] {job['case_name']}"  # build a unique case name
        if (
            self.dry_run
        ):  # we don't want to create anything just show that we would have been
            # able to (probably)
            print(f"[DRY_RUN] Building {case_name}")
            return case_name

        # make the set but it will be empty for now. This allows us to reference the
        # parent set in the items
        self.built_sets[case_name] = self.session.set.add(
            items={},
            meta={
                "batch": self.name,
                "_class": "orcaflex.job",
                "case_name": case_name,
                "state": asdict(data_models.OrcaFlexJobState()),
            },
        )

        # make dicts with data and meta
        opts = dict(
            data=job["job_options"].__dict__, meta={"_class": "orcaflex.job.options"},
        )

        progress = dict(
            data=asdict(data_models.JobProgress("new job")),
            meta={"_class": "orcaflex.job.progress"},
        )
        job_items = {"job_options": opts, "progress": progress}

        # process the data file
        if "data_file" in job:
            if isinstance(
                job["data_file"], Item
            ):  # this is an existing item, update it's batch guid
                existing_item = job["data_file"]
                existing_item["meta"]["case_guid"] = self.built_sets[case_name].guid
            else:
                existing_item = None
                job_items["data_file"] = dict(**job["data_file"])
                job["data_file"]["meta"]["case_guid"] = self.built_sets[case_name].guid
        else:
            existing_item = None

        # add all the required results
        if "required_results" in job:
            result_items = {}
            for rn, rr in enumerate(job["required_results"]):
                res_item = dict(
                    data=rr.to_valid_dict(),
                    meta={
                        "_class": "orcaflex.job.required_result",
                        "case_guid": self.built_sets[case_name].guid,
                    },
                )
                # give the result a name of some kind incase it never actually gets processed
                if rr.meta.name:
                    res_name = f"[{rn}] {rr._type} {rr.meta.name}"
                else:
                    res_name = (
                        f"[{rn}] {rr._type} {rr.object} {rr.variable} {str(rr.period)}"
                    )
                    if hasattr(rr, "arc_length_range"):
                        res_name += f" {str(rr.arc_length_range)}"
                result_items[res_name] = res_item
            if result_items:
                many_results = self.session.item.add_many(
                    list(result_items.values())
                )  # add items
                result_items = dict(
                    zip(
                        result_items.keys(), [r["guid"] for r in many_results["items"]],
                    )
                )  # re-pack
                # results is a mapping of result name to guid of item
                job_items["results"] = dict(
                    data=result_items,
                    meta={
                        "_class": "orcaflex.job.required_results",
                        "case_guid": self.built_sets[case_name].guid,
                    },
                )
        if "load_case_info" in job:
            job_items["load_case_info"] = dict(
                data=asdict(job["load_case_info"]),
                meta={
                    "_class": "orcaflex.job.load_case_info",
                    "case_guid": self.built_sets[case_name].guid,
                },
            )
        if job.get("model_views"):
            model_views = {}
            for _, mv in enumerate(job["model_views"]):
                model_views[mv.ViewName] = asdict(mv)
            # model views data is mapping of view name to ViewParamters type info
            job_items["model_views"] = dict(
                data=model_views,
                meta={
                    "_class": "orcaflex.job.model_views",
                    "case_guid": self.built_sets[case_name].guid,
                },
            )

        job_item_many = self.session.item.add_many(
            list(job_items.values())
        )  # add all the items
        job_items_zipped = dict(
            zip(job_items.keys(), job_item_many["items"])
        )  # re-pack
        if existing_item is not None:
            job_items_zipped[
                "data_file"
            ] = existing_item  # the existing item didn't need to be added so we add it here
        if self.verbose:  # print
            print(f"added {case_name}")
        self.session.log.info(f"created {case_name}")
        self.built_sets[case_name].items = job_items_zipped  # put items on the set
        self.session.set.save(
            self.built_sets[case_name]
        )  # save the set now it has the items
        return case_name

    def _build(self):
        """build the group

        :return:
        """
        self.session.log.info("Building batch...")
        self.built_sets = {}
        # because the time to write to qalx can be slow depending on system load we
        # need to make sure we are adding
        # all our cases concurrently. This can be done with lots of threads because
        # typically we are waiting for
        # a response from the API and not using CPU or io
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.batch_options.build_threads
        ) as executor:
            future_to_job = {
                executor.submit(self._add_case, case_n, job): case_n
                for (case_n, job) in enumerate(self.batch_manager.orcaflex_jobs)
            }
            for future in concurrent.futures.as_completed(future_to_job):
                case_n = future_to_job[future]
                try:
                    case_name = future.result()
                except Exception as exc:
                    self.session.log.error(
                        "%r generated an exception: %s" % (case_n, exc)
                    )
                    raise exc
                else:
                    self.session.log.debug(f"future {case_name}")

    def _submit(self):
        """this is the method that gets called by the BatchManager to submit the batch to a queue"""
        self.session.log.info(f"Submitting batch to {self.batch_options.batch_queue}")
        self.group_batch = self.session.group.add(
            sets=self.built_sets, meta=self.meta
        )  # add the group
        self.session.queue.get_or_create(
            self.batch_options.sim_queue
        )  # create the sim queue if required
        batch_queue = self.session.queue.get_or_create(
            self.batch_options.batch_queue
        )  # do batch queue
        batch_queue.submit_entity(self.group_batch)  # submit batch

    def __enter__(self):
        self.batch_manager = OrcaFlexBatchManager()
        return self.batch_manager

    def __exit__(self, *args):
        self._build()
        self._submit()


class QalxOrcaFlex(pyqalx.QalxSession):
    """we define a sublcass of QalxSession so there is no need to import from pyqalx

    .. warning::

        There are a load of terrible instance methods defined here just because we
        needed some way of doing these things. They need to be superseded by a better
        API

    """

    def __init__(self, *args, **kwargs):
        super(QalxOrcaFlex, self).__init__(*args, **kwargs)

    def get_batch(self, batch_name: str, many: bool = False):
        if many:
            return self.group.find(
                query={
                    "metadata.data._class": "orcaflex.batch",
                    "metadata.data.name": batch_name,
                }
            )["data"]
        else:
            return self.group.find_one(
                query={
                    "metadata.data._class": "orcaflex.batch",
                    "metadata.data.name": batch_name,
                }
            )

    def get_batch_results_summary(
        self, batch_name: str, many: bool = False
    ) -> Union[Sequence[Mapping], Mapping]:
        if many:
            return [
                self.item.get(g["meta"].get("results_summary", {}).get("data", {}))
                for g in self.get_batch(batch_name, many)["data"]
            ]
        else:
            return self.item.get(
                self.get_batch(batch_name, many)["meta"].get("results_summary", {})
            ).get("data", {})

    def get_batch_results_map(
        self, batch_name: str
    ) -> Mapping[str, Mapping[str, Mapping]]:
        res_map = {}
        batch = self.get_batch(batch_name)
        for case_name, j in batch["sets"].items():
            res_map[case_name] = {}
            if j["items"].get("results"):
                for res_name, res_guid in j["items"].get("results")["data"].items():
                    res_map[j.meta.case_name][res_name] = self.item.get(res_guid)[
                        "data"
                    ]
        return res_map

    def save_batch_views(self, batch_name: str, save_dir: PathLike):
        batch = self.get_batch(batch_name)
        for case_name, job in batch["sets"].items():
            if job["items"].get("saved_views"):
                if not isinstance(job["items"].get("saved_views"), Mapping):
                    views = self.item.get(job["items"].get("saved_views"))["data"]
                else:
                    views = job["items"].get("saved_views")["data"]
                for _, view_guid in views.items():
                    view_file = self.item.get(view_guid)
                    save_name = f"{case_name}-{view_file['file']['name']}"
                    view_file.save_file_to_disk(save_dir, filename=save_name)

    def _get_progress(self, job):
        if job["items"].get("progress"):
            if not job["meta"].get("processing_complete"):
                if not isinstance(job["items"].get("progress"), Mapping):
                    prog = self.item.get(job["items"].get("progress"))["data"]
                else:
                    prog = job["items"].get("progress")["data"]
                if prog.get("pretty_time"):
                    return prog["pretty_time"] + " to go."
                else:
                    return prog["progress"]
            else:
                return "complete."

    def _get_state(self, job):
        st_str = job["meta"].get("state", {}).get("state")
        if job["meta"].get("state", {}).get("error"):
            st_str += "\nERROR:"
            st_str += job["meta"].get("state", {}).get("error")
        return st_str

    def _get_warn(self, job):
        if job["items"].get("warnings"):
            if not isinstance(job["items"].get("warnings"), Mapping):
                warns = self.item.get(job["items"].get("warnings"))["data"]
            else:
                warns = job["items"].get("warnings")["data"]
            if warns["warning_text"]:
                return "\n".join(warns["warning_text"])
            else:
                return ""
        else:
            return ""

    def print_batch_progress(self, batch_name: str):
        batch = self.get_batch(batch_name)
        for case_name, job in batch["sets"].items():
            print(case_name, self._get_progress(job))

    def print_batch_state(self, batch_name: str):
        batch = self.get_batch(batch_name)
        for case_name, job in batch["sets"].items():
            print(case_name, self._get_state(job))

    def print_batch_warnings(self, batch_name: str):
        batch = self.get_batch(batch_name)
        for case_name, job in batch["sets"].items():
            print(case_name, self._get_warn(job))

    def print_batch_case_info(self, batch_name: str):
        batch = self.get_batch(batch_name)
        for case_name, job in batch["sets"].items():
            print(case_name, self._get_state(job))
            print(self._get_progress(job))
            print(self._get_warn(job))
