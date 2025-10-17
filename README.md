# `tap-pushbullet`

Singer tap for Pushbullet.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`

## Settings

| Setting | Required | Default | Description |
|:--------|:--------:|:-------:|:------------|
| api_key | True | None | API Key for Geekbot |
| start_date | False | None | Earliest datetime to get data from |
| stream_maps | False | None | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_maps.__else__ | False | None | Currently, only setting this to `__NULL__` is supported. This will remove all other streams. |
| stream_map_config | False | None | User-defined config values to be used within map expressions. |
| faker_config | False | None | Config for the [`Faker`](https://faker.readthedocs.io/en/master/) instance variable `fake` used within map expressions. Only applicable if the plugin specifies `faker` as an additional dependency (through the `singer-sdk` `faker` extra or directly). |
| faker_config.seed | False | None | Value to seed the Faker generator for deterministic output: https://faker.readthedocs.io/en/master/#seeding-the-generator |
| faker_config.locale | False | None | One or more LCID locale strings to produce localized output for: https://faker.readthedocs.io/en/master/#localization |
| flattening_enabled | False | None | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth | False | None | The max depth to flatten schemas. |
| batch_config | False | None | Configuration for BATCH message capabilities. |
| batch_config.encoding | False | None | Specifies the format and compression of the batch files. |
| batch_config.encoding.format | False | None | Format to use for batch files. |
| batch_config.encoding.compression | False | None | Compression format to use for batch files. |
| batch_config.storage | False | None | Defines the storage layer to use when writing batch files |
| batch_config.storage.root | False | None | Root path to use when writing batch files. |
| batch_config.storage.prefix | False | None | Prefix to use when writing batch files. |

A full list of supported settings and capabilities is available by running: `tap-pushbullet --about`

### Source Authentication and Authorization



## Usage

You can easily run `tap-pushbullet` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-pushbullet --version
tap-pushbullet --help
tap-pushbullet --config CONFIG --discover > ./catalog.json
```
## Developer Resources

### Initialize your Development Environment

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already.

### Create and Run Tests

Create tests within the `tests` subfolder and then run:

```bash
uv run pytest
```

You can also test the `tap-pushbullet` CLI interface directly using `uv run`:

```bash
uv run tap-pushbullet --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Use Meltano to run an EL pipeline:

```bash
# Test invocation:
uvx meltano invoke tap-pokemon --version

# OR run a test `elt` pipeline:
uvx meltano run tap-pokemon target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
