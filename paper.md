---
title: 'PyMedPhys: A community effort to develop an open, Python-based standard library for medical physics applications'
tags:
  - Python
  - Medical Physics
  - Radiation Therapy
  - Diagnostic Imaging
  - DICOM
authors:
  - name: Simon Biggs
    affiliation: 1
    orcid: 0000-0003-2058-7868
  - name: Matthew Jennings
    affiliation: 2
    orcid: 0000-0002-1288-2683
  - name: Stuart Swerdloff
    affiliation: 3
    orcid: 0000-0003-0754-4679
  - name: Phillip Chlap
    affiliation: '4, 5'
    orcid: 0000-0002-6517-8745
  - name: Derek Lane
    affiliation: 6
    orcid: 0000-0002-4148-1213
  - name: Jacob Rembish
    affiliation: 7
    orcid: 0000-0002-6508-4175
  - name: Jacob McAloney
    affiliation: 8
    orcid: 0000-0001-8060-6907
  - name: Paul King
    affiliation: 9
    orcid: 0000-0001-6748-4538
  - name: Rafael Ayala
    affiliation: 10
    orcid: 0000-0001-6925-6176
  - name: Fada Guan
    affiliation: 11
    orcid: 0000-0001-8477-7391
  - name: Nicola Lambri
    affiliation: '12, 13'
    orcid: 0000-0001-8706-6480
  - name: Cody Crewson
    affiliation: 14
  - name: Matthew Sobolewski
    affiliation: '8, 15'
affiliations:
  - name: Radiotherapy AI, Wagga Wagga, Australia
    index: 1
  - name: The Royal Adelaide Hospital, Adelaide, Australia
    index: 2
  - name: ELEKTA Pty Ltd, Auckland, New Zealand
    index: 3
  - name: University of New South Wales, Sydney, Australia
    index: 4
  - name: Ingham Institute for Applied Medical Research, Liverpool, Australia
    index: 5
  - name: Elekta AB, Stockholm, Sweden
    index: 6
  - name: NYU Langone Health, New York, New York, United States of America
    index: 7
  - name: Riverina Cancer Care Centre, Wagga Wagga, Australia
    index: 8
  - name: Painless Skin Cancer Treatment Center, Meridian, Mississippi, United States of America
    index: 9
  - name: Hospital G.U. Gregorio Marañón, Madrid, Spain
    index: 10
  - name: Yale University School of Medicine, New Haven, Connecticut, United States of America
    index: 11
  - name: IRCCS Humanitas Research Hospital, Milan, Italy
    index: 12
  - name: Humanitas University, Milan, Italy
    index: 13
  - name: Saskatchewan Cancer Agency, Saskatoon, Canada
    index: 14
  - name: CancerCare Partners, Sydney, Australia
    index: 15
date: 10 February 2022
bibliography: paper.bib
---

# Summary

PyMedPhys is an open-source medical physics library built for Python by a
diverse community that values and prioritizes code sharing, review,
continuous improvement, and peer development. PyMedPhys aims to simplify
and enhance both research and clinical work related to medical physics. It
is inspired by the Astropy Project [@astropy]; a highly successful
collaborative work of our physics peers in astronomy.

# Statement of need

Medical radiation applications are subject to fast-paced technological
advancements. This is particularly true in the field of radiation oncology,
where the implementation of increasingly sophisticated technologies requires
increasingly complex processes to maintain the improving standard of care. To
help address this challenge, software tools that improve the quality, safety
and efficiency of clinical tasks are increasingly being developed in-house
[@kuo2020JACMP; @Maughan2019MP; @Arumugam2016MP; @Edvardsson2018PMB; @LiJS2010MP;
@Bakhtiari2011MP; @Latala2020MD; @Bhagroo2019MP; @Huang2021JACMP; @Chan2015TCRT;
@Skouboe2019RO; @Kimura2021MP; @Inaniwa2018PMB; @Keall2014MP].
Commercial options are often prohibitively expensive or insufficiently tailored
to an individual clinic's needs. On the other hand, in-house development
efforts are often limited to a single institution. Similar tools that could
otherwise be shared are instead "reinvented" in clinics worldwide on a routine
basis. Moreover, individual institutions typically lack the personnel and
resources to incorporate simple aspects of good development practice or to
properly maintain in-house software.

By creating and promoting an open-source repository, PyMedPhys aims to improve
the quality and accessibility of existing software solutions to problems faced
across a range of medical radiation applications, especially those
traditionally within the remit of medical physicists. These solutions can be
broadly categorised in two areas: data extraction/conversion of proprietary
formats from a variety of radiotherapy systems, and manipulation of standard
radiotherapy data to perform quality assurance (QA) tasks that are otherwise
time-consuming or lack commercial solutions with the desired flexibility or
true function.

Data extraction and conversion currently includes: two treatment planning
systems, an oncology information system, and a linear accelerator vendor
family of systems. Data in proprietary formats from these systems are
extracted and converted to allow for integration in a myriad of applications.
Applications that use planning system information include: electron cut-out
factor determination, CT extension, and extraction of dose information for
patient QA purposes. Applications that use the oncology information systems
include: clinical dashboards that summarise data, quality task tracking, and
comparison of dose information to planning systems. Applications that use the
linear accelerator data include: patient specific QA analysis against planning
data, and analysis of machine performance such as the Winston-Lutz test.

QA tasks using standard radiotherapy data include: anonymisation, extraction
of dose data for analysis, manipulation of contour files to allow merging or
adjustments/scaling of relative electron density, modifying machine names
in plans, and most frequently used, the calculation of a Gamma index, a widely
recognised metric in radiotherapy analysis that quantifies the difference
between measured and calculated dose distributions on a point-by-point basis
in terms of both dose and distance to agreement (DTA) differences.

Many of these tools are in use clinically at affiliated sites, and
additionally, aspects of PyMedPhys are implemented around the world for some
applications. Many parties have embraced the gamma analysis module
[@milan2019evaluation; @galic2020method; @rodriguez2020new; @cronholm2020mri;
@spezialetti2021using; @tsuneda2021plastic; @pastor2021learning;
@gajewski2021commissioning; @lysakovski2021development; @castle2022; @yang2022PMB],
while implementations of the electron cutout factor module and others
[@baltz2021validation; @rembish2021automating; @douglass2021deepwl] have also
been reported. Additionally, the work has been recognized by the European
Society for Radiotherapy and Oncology (ESTRO) and referenced as recommended
literature in their 3rd Edition of Core Curriculum for Medical Physics Experts
in Radiotherapy [@bertcatharine].

# Acknowledgements

We acknowledge the support of all who have contributed to the development of
PyMedPhys along the way.

# References
