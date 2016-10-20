# Preface #

This document describes the functionality provided by the xlr-ispw-plugin.

See the **[XL Release Documentation](https://docs.xebialabs.com/xl-release/index.html)** for background information on XL Release and release concepts.

# CI status #

[![Build Status][xlr-ispw-plugin-travis-image]][xlr-ispw-plugin-travis-url]
[![Codacy Badge][xlr-ispw-plugin-codacy-image] ][xlr-ispw-plugin-codacy-url]
[![Code Climate][xlr-ispw-plugin-code-climate-image] ][xlr-ispw-plugin-code-climate-url]

[xlr-ispw-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-ispw-plugin.svg?branch=master
[xlr-ispw-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-ispw-plugin
[xlr-ispw-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/36153ed9460a44d289aa1186cde51fa1
[xlr-ispw-plugin-codacy-url]: https://www.codacy.com/app/joris-dewinne/xlr-ispw-plugin
[xlr-ispw-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-ispw-plugin/badges/gpa.svg
[xlr-ispw-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-ispw-plugin


# Overview #

# Installation #

* Minimal version XLR: 5.0.0+

## Tasks ##
+ CreateRelease
  + `srid`: The instance of ISPW you are working with.
  + `Application`:
  + `Stream`:
  + `Release description`:
  + `Release id`: 8 character Release id.
  + `Release prefix`: 8 character Release prefix.
  + `Owner`:
  + `Reference Number`:
  ![XLR Create Release](images/CreateRelease.png)
+ GetReleaseInformation
  + `srid`: The instance of ISPW you are working with.
  + `Release id`: 8 character Release id.
  ![XLR Get Release Information](images/GetReleaseInfo.png)
+ Promote
+ Deploy
+ GetSetInformation