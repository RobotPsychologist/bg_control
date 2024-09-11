# Data Dictionary

Example1: 2024-05-01 09:46:39.884000-05:00,1057.0,101.0,1714574729090.0,Dosed 4u,,DOSE_INSULIN,False,True,4.0,,,False,,,Message

Example2: 2024-05-01 14:26:03.470000-05:00,1057.0,88.0,1714590328750.0,6gGlucose,,INTERVENTION_SNACK,True,False,,6.0,1.0,False,,,Message,

| Field Name | Datatype | Description |
| -------- | ------- | ------- |
|  date | timeseries | Time of blood glucose level reading. |
| sender_id | N/A | ignore |
| bgl | int4 | blood glucose level (in units of mg/dL) |
| bgl_date_millis | milliseconds | When a message is logged, there is an associated bgl. This field is the millisecond value for when that bgl reading is from. |
| text | text | If a message is logged, this is the text associated with it. E.g. "Dosed 2u 25m ago" |
| template | enum | Some messages are logged automatically via third party integrations, like the Omnipod 5, Apple Healthkit, or Nightscout. If this field is not null, it means the message was logged via one of these third party tools so the 'text' column will be interpreted as JSON. |
| msg_type | enum | The type of message being logged. Possible values include (but are not limited to) ANNOUNCE_MEAL, DOSE_INSULIN, DOSE_BASAL_INSULIN, BGL_FP_READING, INTERVENTION_SNACK, etc. |
| affects_fob | bool | fob: food on board. E.g. if the message is a meal announcement, then this column will be true. |
| affects_iob | bool | iob: insulin on board, the amount of insulin administered that the PWD has not yet absorbed. |
| dose_units | float8 | Number of units of insulin administered. |
| food_g | float8 | The number of grams of carbohydrates being logged. |
| food_glycemic_index | float8 | The glycemic index of the carbohydrates. Currently there are only two values used - 0.5 for regular meal announcements, or 1 for INTERVENTION_SNACKS (typically higher glycemic foods like glucose tabs, candy, juice, etc.) |
| dose_automatic | bool | Indicates if the insulin dose was automatically administered (like via an OP5 pump itegration) or not. |
| fp_bgl | int4 | Finger prick blood glucose level. Sometimes, when the continuous glucose monitor (CGM) isn't working the PWD will take a blood glucose reading by stabbing their finger and measuring the sugar from the blood directly. Some users may not have a CGM at all, in which case fp_bgl is the only indication of their bgl. |
| message_basal_change |  | (ignore) Automatically logged changes in basal insulin dose. Basal insulin is the amount of baseline slow acting insulin the PWD takes each day. |
| __typename | enum | What the type is for the row (message? bgl reading?). Not as important, since it can be derived from / overlaps with msg_type in some cases. |
| trend | enum | The direction the blood glucose level is changing (FLAT, SINGLE_UP, DOUBLE_UP, FORTYFIVE_UP, FORTYFIVE_DOWN, NOT_COMPUTABLE, etc.). This is reported by the CGM sensor itself in most cases. |
