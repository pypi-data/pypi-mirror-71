# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.10.0] - 2019-12-26

### Added

* Add `webserver static add` script that rsync's static files for website to use

## [0.9.1] - 2019-12-26

### Added

* Add `webserver conf reload` script that tests and reloads configurations w/o downtime

## [0.9.0] - 2019-12-26

### Added

* Add `webserver conf create` script that uses `webserver genconf` and adds config
* Add `webserver conf edit` script that open editor with website configuration

## [0.8.2] - 2019-12-26

### Changed

* Make `webserver genconf` output comment with version of webserver that was used

### Added

* Add -q/--quiet flag to `webserver genconf` to silence explanations output

## [0.8.0] - 2019-12-25

### Added

* Add sites.py (`webserver sites`) script group that deals with configurations

## [0.7.0] - 2019-12-25

### Added

* Add gendh.py (`webserver gendh`) script that generates 3072 DH params for website

## [0.6.2] - 2019-12-25

### Fixed

* Removed $ that was needed in Bash script from `webserver gentls` script

## [0.6.1] - 2019-12-25

### Changed

* Command `webserver gentls` is now using sudo

## [0.6.0] - 2019-12-25

### Added

* Add gentls.py (`webserver gentls`) script that gets LetsEncrypt TLS certificate for website

## [0.5.0] - 2019-12-25

### Changed

* Command `webserver sites genconf` is now simplified to `webserver genconf`

## [0.4.2] - 2019-12-24

### Added

* Add genconf.py (`webserver sites genconf`) script that generates HTTPS config with examples

## [0.3.1] - 2019-12-23

### Added

* Add -q/--quiet flag to `webserver update` to silence output
* Add --no-pull flag to `webserver update` to skip pulling fresh nginx image

## [0.3.0] - 2019-12-23

### Added

* Add -q/--quiet flag to `webserver run` to silence output
* Add --no-pull flag to `webserver run` to skip pulling fresh nginx image

## [0.2.1] - 2019-12-22

### Changed

* Start using green-colored text by adding click.style() in click.echo()

## [0.2.0] - 2019-12-22

### Added

* Add update.py (`webserver update`) script that updates webserver stack images

## [0.1.1] - 2019-12-22

### Added

* Add echo to run script with explanation of what script does at certain moment

## [0.1.0] - 2019-12-21

### Added

* Add run.py (`webserver run`) script that spins up nginx stack on Docker Swarm

### Removed

* Folders that were used for Bash scripts are now removed
