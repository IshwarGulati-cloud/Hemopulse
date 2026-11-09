GRANT SELECT ON public.healthcare_facilities TO anon;

DROP POLICY IF EXISTS "Allow anon to read healthcare facilities"
ON public.healthcare_facilities;

CREATE POLICY "Allow anon to read healthcare facilities"
ON public.healthcare_facilities
FOR SELECT
TO anon
USING (true);
