# tap-swellrewards
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Versions](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)](https://pypi.python.org/pypi/ansicolortags/)

A [Singer](https://www.singer.io/) tap for extracting data from the [Swell Rewards API](https://loyaltyapi.yotpo.com/reference).

## Installation

Since package dependencies tend to conflict between various taps and targets, Singer [recommends](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-singer-with-python) installing taps and targets into their own isolated virtual environments:

### Install SwellRewards Tap

```bash
$ cd tap-swellrewards
$ python3 -m venv ~/.venvs/tap-swellrewards
$ source ~/.venvs/tap-swellrewards/bin/activate
$ pip3 install tap-swellrewards # or pip3 install .
$ deactivate
```

### Install Singer Target

```bash
$ python3 -m venv ~/.venvs/target-stitch
$ source ~/.venvs/target-stitch/bin/activate
$ pip3 install target-stitch
$ deactivate
```

## Configuration

The tap accepts a JSON-formatted configuration file as arguments. This configuration file has three required fields:

1. `api_key`: A valid Swell Rewards API Key (found in the Settings of your Swell account)
2. `api_guid`: A valid Swell Rewards API GUID (found in the Settings of your Swell account)
3. `start_date` The `start_date` parameter determines the starting date for the last registered customer activity within the Yotpo loyalty and rewards system e.g. purchase, redemption, etc. For example, pass a value of `2019-01-01` to fetch active customers since January 1st, 2019. 

An bare-bones SwellRewards confirguration may file may look like the following:

```json
{
  "api_key": "abaoEFoiahwef12425",
  "api_guid": "YAYAHbafoiafoH235",
  "start_date": "2019-01-21"
}
```

## Streams

The current version of the tap syncs one distinct [Stream](https://github.com/singer-io/getting-started/blob/master/docs/SYNC_MODE.md#streams):
1. `Customers`: ([Endpoint](https://loyaltyapi.yotpo.com/reference#customers))

## Discovery

Singer taps describe the data that a stream supports via a [Discovery](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode) process. You can run the SwellRewards tap in Discovery mode by passing the `--discover` flag at runtime:

```bash
$ ~/.venvs/tap-swellrewards/bin/tap-swellrewards --config=config/swellrewards.config.json --discover
```

The tap will generate a [Catalog](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#the-catalog) to stdout. To pass the Catalog to a file instead, simply redirect it to a file:

```bash
$ ~/.venvs/tap-swellrewards/bin/tap-swellrewards --config=config/swellrewards.config.json --discover > catalog.json
```

## Sync Locally

Running a tap in [Sync mode](https://github.com/singer-io/getting-started/blob/master/docs/SYNC_MODE.md#sync-mode) will extract data from the various Streams. In order to run a tap in Sync mode, pass a configuration file and catalog file:

```bash
$ ~/.venvs/tap-swellrewards/bin/tap-swellrewards --config=config/swellrewards.config.json --catalog=catalog.json
```

The tap will emit occasional [State messages](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md#state-message). You can persist State between runs by redirecting State to a file:

```bash
$ ~/.venvs/tap-swellrewards/bin/tap-swellrewards --config=config/swellrewards.config.json --catalog=catalog.json >> state.json
$ tail -1 state.json > state.json.tmp
$ mv state.json.tmp state.json
```

To pick up from where the tap left off on subsequent runs, simply supply the [State file](https://github.com/singer-io/getting-started/blob/master/docs/CONFIG_AND_STATE.md#state-file) at runtime:

```bash
$ ~/.venvs/tap-swellrewards/bin/tap-swellrewards --config=config/swellrewards.config.json --catalog=catalog.json --state=state.json >> state.json
$ tail -1 state.json > state.json.tmp
$ mv state.json.tmp state.json
```

## Sync to Stitch

You can also send the output of the tap to [Stitch Data](https://www.stitchdata.com/) for loading into the data warehouse. To do this, first create a JSON-formatted configuration for Stitch. This configuration file has two required fields:
1. `client_id`: The ID associated with the Stitch Data account you'll be sending data to.
2. `token` The token associated with the specific [Import API integration](https://www.stitchdata.com/docs/integrations/import-api/) within the Stitch Data account.

An example configuration file will look as follows:

```json
{
  "client_id": 1234,
  "token": "foobarfoobar"
}
```

Once the configuration file is created, simply pipe the output of the tap to the Stitch Data target and supply the target with the newly created configuration file:

```bash
$ ~/.venvs/tap-swellrewards/bin/tap-swellrewards --config=config/swellrewards.config.json --catalog=catalog.json --state=state.json | ~/.venvs/target-stitch/bin/target-stitch --config=config/stitch.config.json >> state.json
$ tail -1 state.json > state.json.tmp
$ mv state.json.tmp state.json
```

Copyright &copy; 2020 Stitch
