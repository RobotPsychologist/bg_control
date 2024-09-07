# Data Dictionary

Example1: 2024-05-01 09:46:39.884000-05:00,1057.0,101.0,1714574729090.0,Dosed 4u,,DOSE_INSULIN,False,True,4.0,,,False,,,Message
Example: 2024-05-01 14:26:03.470000-05:00,1057.0,88.0,1714590328750.0,6gGlucose,,INTERVENTION_SNACK,True,False,,6.0,1.0,False,,,Message,

| Field Name | Datatype | Description |
| -------- | ------- | ------- | 
|  date | timeseries | Time of blood glucose level reading. |
| sender_id | N/A | ignore | 
| bgl |  | blood glucose level |
| bgl_date_millis | | |
| text | | |
| template | | |
| msg_type | | |
| affects_fob | | fob: food on board, ... |
| affects_iob | | iob: insulin on board, the amount of insulin administered that the PWD has not yet absorbed. |
| dose_units | | Number of units of insulin administered. |
| food_g | | |
| food_glycemic_index | |  |
| dose_automatic | | |
| fp_bgl | | |
| message_basal_change | | Change in basal insulin dose. Basal insulin is the amount of baseline slow acting insulin the PWD takes each day. |
| __typename | | |
| trend | | the direction the blood glucose level is changing. |
