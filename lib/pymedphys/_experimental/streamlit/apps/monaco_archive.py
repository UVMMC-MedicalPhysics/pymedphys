# Copyright (C) 2021 Cancer Care Associates

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
import shutil
import time

from pymedphys._imports import numpy as np
from pymedphys._imports import streamlit as st

from pymedphys._streamlit import categories
from pymedphys._streamlit import utilities as _utilities
from pymedphys._streamlit.utilities import config as st_config

CATEGORY = categories.PLANNING
TITLE = "Monaco Archive Tool"


def main():
    # TODO: Make a way to scope session state on a per/app basis.
    session_state = _utilities.session_state(
        patient_directories=tuple(), weeks_since_touched=dict()
    )

    config = st_config.get_config()

    site_directory_map = {}
    for site_config in config["site"]:
        site = site_config["name"]
        try:
            site_directory_map[site] = {
                "focal_data": site_config["monaco"]["focaldata"],
                "clinic": site_config["monaco"]["clinic"],
                "holding": site_config["monaco"]["archive_holding"],
                "destination": site_config["monaco"]["archive_destination"],
            }
        except KeyError:
            continue

    chosen_site = st.radio("Site", list(site_directory_map.keys()))
    directories = site_directory_map[chosen_site]

    focal_data = pathlib.Path(directories["focal_data"])
    clinic = focal_data.joinpath(directories["clinic"])
    holding = focal_data.joinpath(directories["holding"])

    destination = pathlib.Path(directories["destination"])

    finding_patient_directories = st.button("Find Patient Directories")
    if finding_patient_directories:
        session_state.patient_directories = tuple(
            demographic_file.parent
            for demographic_file in clinic.glob("*~*/demographic.*")
        )

    patient_directories = session_state.patient_directories
    if len(patient_directories) == 0:
        st.stop()

    directory_names = [directory.name for directory in patient_directories]

    patient_files_expander = st.beta_expander(
        "All patient directories", expanded=finding_patient_directories
    )
    with patient_files_expander:
        id_sorted_directory_names = sorted(
            directory_names, key=_patient_directory_sort_key
        )
        _print_list_of_ids(id_sorted_directory_names)

    st.write("---")

    determine_weeks_since_touched = st.button(
        "Calculate weeks since touched via sub-directory modified check"
    )

    if determine_weeks_since_touched:
        weeks_sinces_touched = _weeks_since_touched(patient_directories)
        session_state.weeks_since_touched = weeks_sinces_touched

    weeks_sinces_touched = session_state.weeks_since_touched

    def _get_weeks(patient_directory):
        return weeks_sinces_touched[clinic.joinpath(patient_directory)]

    if len(weeks_sinces_touched.keys()) == 0:
        st.stop()

    weeks_since_touched_expander = st.beta_expander(
        "Weeks since touched", expanded=determine_weeks_since_touched
    )

    def _display_directory_names(directory_names):
        directory_names_by_weeks_since_touched = sorted(
            directory_names, key=_get_weeks, reverse=True
        )

        item_markdown = [
            f"* Patient Directory: `{directory}` | Weeks since modified: `{_get_weeks(directory):.2f}`"
            for directory in directory_names_by_weeks_since_touched
        ]

        st.write("\n".join(item_markdown))

    with weeks_since_touched_expander:
        _display_directory_names(directory_names)

    st.write("---")

    try:
        default_weeks_to_keep = config["monaco_archiving"]["default_weeks_to_keep"]
    except KeyError:
        default_weeks_to_keep = 52

    weeks_to_keep = st.number_input(
        "Number of weeks to keep", min_value=0, value=default_weeks_to_keep
    )
    directories_to_archive = _determine_directories_to_archive(
        weeks_sinces_touched, weeks_to_keep
    )
    directory_names_to_archive = [
        directory.name for directory in directories_to_archive
    ]

    _display_directory_names(directory_names_to_archive)

    testing_final_locations = [
        destination.joinpath(name) for name in directory_names_to_archive
    ]

    allow_move_button = True

    for directory in directories_to_archive:
        if not directory.exists():
            st.warning(f"`{directory}` does not exist anymore.")

        allow_move_button = False

    for directory in testing_final_locations:
        if directory.exists():
            st.warning(
                f"The final intended destination of `{directory}` already exists."
            )

        allow_move_button = False

    intermediate_holding_locations = [
        holding.joinpath(name) for name in directory_names_to_archive
    ]

    st.write(
        f"""
        ## The moving plan

        Once the below button is pressed this application will undergo
        the moves detailed below. These moves are into the holding
        directory of `{holding}`. This is not their intended final
        location. Once the button below has been pressed use your OS's
        file explorer to move these files to their final location of
        `{destination}`. Then, once complete, utilise the final test
        button to confirm that the move was as expected.
        """
    )

    moving_plan = list(zip(directories_to_archive, intermediate_holding_locations))

    plan_to_move_details = [
        f"* `{from_dir}` => `{to_dir}`" for from_dir, to_dir in moving_plan
    ]
    st.write("\n".join(plan_to_move_details))

    holding_directory_contents = list(holding.glob("*"))
    if len(holding_directory_contents) != 0:
        st.warning(
            f"The holding directory, `{holding}`, is not empty. Unable "
            "to place more files within this directory until those files "
            f"been moved to `{destination}`"
        )

        allow_move_button = False

    if allow_move_button:
        if st.button("Undergo move"):
            for from_dir, to_dir in moving_plan:
                shutil.move(from_dir, to_dir)

    if st.button("Test moves"):
        directories_left_behind = []
        directories_not_in_archive = []
        for from_dir, to_dir in zip(directories_to_archive, testing_final_locations):
            if from_dir.exists():
                directories_left_behind.append(from_dir)
                st.error(f"`{from_dir}` was left behind.")

            if not to_dir.exists():
                directories_not_in_archive.append(to_dir)
                st.error(f"`{to_dir}` was not found in archive.")

        if not directories_left_behind and not directories_not_in_archive:
            st.success("All planned moves appeared to have been successful.")


def _patient_directory_sort_key(patient_directory_name):
    prepended_number, patient_id = patient_directory_name.split("~")
    return f"{patient_id}.{prepended_number.zfill(6)}"


def _print_list_of_ids(ids):
    markdown = "`\n* `".join(ids)
    st.write(f"* `{markdown}`")


def _weeks_since_touched(patient_directories):
    status_indicator = st.empty()
    progress_bar = st.progress(0)

    now = time.time()

    weeks_sinces_touched = {}

    for i, current_patient_directory in enumerate(patient_directories):
        status_indicator.write(f"Patient Directory: `{current_patient_directory.name}`")

        paths_to_check = list(current_patient_directory.glob("*")) + list(
            current_patient_directory.joinpath("plan").glob("*")
        )
        modified_times = np.array([os.path.getmtime(item) for item in paths_to_check])

        number_of_weeks_ago = (now - modified_times) / (60 * 60 * 24 * 7)
        minimum_number_of_weeks_ago = np.min(number_of_weeks_ago)

        weeks_sinces_touched[current_patient_directory] = minimum_number_of_weeks_ago
        progress = (i + 1) / len(patient_directories)
        progress_bar.progress(progress)

    return weeks_sinces_touched


@st.cache
def _determine_directories_to_archive(weeks_sinces_touched, weeks_to_keep):
    directories_to_archive = []
    for directory, weeks in weeks_sinces_touched.items():
        if weeks > weeks_to_keep:
            directories_to_archive.append(directory)

    return directories_to_archive
