Air Traffic Data Processing Pipeline
-------------------------------------

This project provides a structured pipeline to collect, process, and optionally filter air traffic data using the OpenSky Network API. The steps below describe the proper sequence and dependencies for using the available scripts.

Required Setup
--------------

0. **Environment Setup**
   - Ensure you have a working Python/Conda environment.
   - Install the required packages using the following command:
     ```
     pip install -r requirements.txt
     ```
     or
     ```     
     conda install --yes --file requirements.txt
     ```
   - You must also have a valid OpenSky API setup with appropriate access credentials.

Processing sequence
-------------------

1. **Airspace Definition**
   - Script: `airspace_definition.py`
   - Purpose: Define the geographical bounds (regions or sectors) to be used in data retrieval.
   - Output: A dictionary or data structure with airspace definitions used as input in the next step.

2. **Historical Traffic Data Collection**
   - Script: `historical_traffic_data.py`
   - Purpose: Retrieve air traffic data from OpenSky within the defined airspaces and time intervals.
   - Input: Airspace definitions from `airspace_definition.py`
   - Output: Raw flight data stored in a `.csv` file.

3. **Air Traffic Preprocessing**
   - Script: `air_traffic_pre_processing.py`
   - Purpose: Process the raw data to assign flight identifiers (`flight_id`), filter noise, and assign uniform time steps.
   - Output: Cleaned and structured dataset ready for analysis or filtering.

4. **Optional Flight Selection**
   - Script: `00_flight_selection.py`
   - Purpose: Select flights of interest based on specific callsigns.
   - Input: Processed flight data from the previous step.
   - Output: Filtered dataset containing only the selected callsigns.

5. **Optional Airframe Selection**
   - Script: `00_airframe_selection.py`
   - Purpose: Select flights based on specific aircraft characteristics (e.g., airframe types).
   - Input: Output from previous steps or full dataset.
   - Output: Further refined dataset based on aircraft criteria.

Notes
-----

- Ensure scripts are executed in the correct order to avoid inconsistencies in the dataset.
- Intermediate results (especially from steps 2 and 3) are saved to disk and reused in later steps.
- Optional filtering steps (4 and 5) are useful for focused analysis or targeted studies.

Contact
-------

For questions or contributions, please contact: wesley.silva@tecnico.ulisboa.pt
