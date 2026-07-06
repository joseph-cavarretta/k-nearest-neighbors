# Finding closest pairs of coordinates from two arrays

[![CI](https://github.com/joseph-cavarretta/k-nearest-neighbors/actions/workflows/ci.yml/badge.svg)](https://github.com/joseph-cavarretta/k-nearest-neighbors/actions/workflows/ci.yml)

An optimized approach for point-distance matching across two arrays of
coordinates — first as an analysis notebook, then productized as an HTTP API.

In one of my previous roles, I encountered a problem where for a list of tens of thousands of locations, I needed to find the nearest location to it from another list with thousands of potential matches (using latitude and longitude)

Initially, I used a k-nearest neighbors pairwise approach to find the distance of every location to every other location and keep the smallest distance for each one. But with over 10,000 locations in each list, this brute force method (O(n<sup>2</sup>)) took several hours (and Gb of memory) to run.

After some additional research, I was able to optimize my approach to run in under 1 minute by utilizing a Ball Tree Algorithm.
A Ball Tree works by partitioning the space of the training data (in this case 2-dimensional) into circular blocks (balls) and compares each point only to nearby points to find the closest.

Using a US housing dataset and a list of all Starbucks locations in the US, I've recreated this problem using both approaches in the `k_nearest_neighbors.ipynb` file.

## Finding the Closest Starbucks to Houses in the US

What's the fastest way to find the closest Starbucks to any house in the US?

**Runtime to find the closest Starbucks to each house using brute force?** 20 minutes 24 seconds.

**Runtime using the Ball Tree?** 1.44 seconds!

**Average distance to a Starbucks from over 27,000 houses in the US?** 8.15 miles :)

## Running the Notebook

```bash
# install dependencies with uv
make install    # uv sync

# launch notebook
make notebook   # uv run jupyter notebook k_nearest_neighbors.ipynb
```

## The API

The Ball Tree matching is also exposed as a FastAPI service so the analysis
runs as a real endpoint: send two lists of coordinates — the points you're
querying for and the reference points to match against — and get back each
query point's nearest reference points, with distances and per-request timing.

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/v1/neighbors` | Return the `k` nearest reference points for each query point |
| `GET` | `/healthz` | Liveness probe — the process is serving |
| `GET` | `/readyz` | Readiness probe — runs a real Ball Tree query end to end |

Interactive docs are served at `/docs` when the app is running.

### Running it

```bash
make api          # uvicorn dev server on http://localhost:8000

# or containerized
make docker-up    # docker compose up -d  (http://localhost:8000)
make docker-down
```

### Example

```bash
curl -X POST http://localhost:8000/v1/neighbors \
  -H 'Content-Type: application/json' \
  -d '{
    "query_points": [{"lat": 40.014986, "lon": -105.270546}],
    "reference_points": [
      {"lat": 37.7749, "lon": -122.4194},
      {"lat": 39.739236, "lon": -104.984862}
    ],
    "k": 1,
    "unit": "miles"
  }'
```

```json
{
  "results": [
    {
      "query_index": 0,
      "neighbors": [
        {
          "reference_index": 1,
          "coordinate": {"lat": 39.739236, "lon": -104.984862},
          "distance": 24.341963358502785
        }
      ]
    }
  ],
  "query_count": 1,
  "reference_count": 2,
  "k": 1,
  "unit": "miles",
  "elapsed_ms": 0.43
}
```

Coordinates are decimal degrees (latitude `-90..90`, longitude `-180..180`).
`k` defaults to `1` and must not exceed the number of reference points; `unit`
is `miles` (default) or `kilometers`. Distances use the haversine metric on a
sphere, matching the notebook.

### Configuration

Settings are read from the environment (see `.env.example`):

| Variable | Default | Purpose |
|---|---|---|
| `MAX_POINTS_PER_LIST` | `50000` | Reject requests with more points than this per list (HTTP 413) |
| `BALLTREE_LEAF_SIZE` | `40` | Ball Tree leaf size (sklearn default) |
| `LOG_LEVEL` | `INFO` | Application log level |

## Development

```bash
make test         # pytest
make check        # ruff lint + format check
make type-check   # mypy
```

Source lives under `src/` (`config/` settings, `models.py`, `libs/` core
algorithm, `app/` FastAPI wiring). The notebook remains the analysis artifact.

## Dependencies

| Package | Purpose |
|---|---|
| `scikit-learn` | Ball Tree implementation (`sklearn.neighbors.BallTree`) |
| `numpy` | Array operations and degree→radian conversion |
| `fastapi` / `uvicorn` | HTTP API and ASGI server |
| `pydantic` / `pydantic-settings` | Request/response models and configuration |
| `pandas` | Data loading in the notebook (dev dependency) |
