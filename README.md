# HemoPulse backend

FastAPI backend for the HemoPulse anemia screening project. The prediction model and four risk labels are a **demo only**; they are not medically validated and must not guide care.

## Setup

Use Python 3.12, then from the project folder run:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add the Supabase project URL and anon key to `.env`. Keep `.env` private; never commit it.

## Run the API

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation. `GET /` is the health check.

### Endpoints

- `POST /api/v1/predict/eyelid` accepts `red_ratio`, `green_ratio`, and `blue_ratio` percentages as JSON.
- `POST /api/v1/predict/eyelid/image` accepts a JPEG or PNG up to 5 MB in the `photo` multipart field. It uses a centered crop as a demo approximation; it does not locate or segment the conjunctiva.
- `GET /api/v1/facilities/` lists facilities. Optional filters: `level` (1–3), `latitude` and `longitude` together, and `radius_km`.

Predictions include `demo_only: true`. The image and RGB endpoints return four labels, but those labels are provisional. `confidence_score` is the model's highest class probability; it has not been calibrated and should not be interpreted as clinical certainty.

## Supabase facilities access

The backend uses the anon key for read-only access to `public.healthcare_facilities`. Run [`supabase/grant_facility_catalog_read.sql`](supabase/grant_facility_catalog_read.sql) in the Supabase SQL Editor. It grants `SELECT` and adds an RLS read policy for `anon`. The demo prediction endpoint does not write to `screening_logs`.

## Train the demo model

Keep the CSV local; it contains personal names and should not be committed. With the dataset at `C:\Users\<you>\Downloads\anemia_dataset.csv`, run:

```powershell
python train_model.py "C:\Users\<you>\Downloads\anemia_dataset.csv"
```

The script uses `%Red Pixel`, `%Green pixel`, and `%Blue pixel` as features. It splits the dataset's `Hb` values at that dataset's 25th, 50th, and 75th percentiles and names the resulting bins Severe, Moderate, Mild, and Normal. These cohort-based bins are not WHO cutoffs or validated clinical labels. The script saves the model and cutoffs to `app/models/hemopulse_model.pkl` and reports five-fold cross-validated balanced accuracy. The current dataset has 104 records; its reported score is only a small-sample demo estimate.

The CSV is not included in this repository. Re-training requires a local copy with the three RGB columns and `Hb`.

## Current limits

This backend is ready for a project demo, not clinical use or public deployment. The current dataset has only 104 records and lacks the age/sex/pregnancy context needed to choose appropriate clinical cutoffs. Do not publish that CSV: it contains names alongside hemoglobin values. Keep it on a private local drive and use only data you have permission to process. Before connecting a public frontend, replace wildcard CORS with that frontend's exact origin. A clinically meaningful model requires an approved, de-identified dataset with documented labels and validation on separate data.
