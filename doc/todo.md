# Current issues

## problem 
* file upload: file size
* flask log in apache as seen as error file

## todo
* sync title and status (via bot)
* format the dump (array, pdf...) + file attachement
* dashboard autorefresh (or use default loading on the main web page)
* bot log msg in the local db (or dump Space?)
* webhook delete (useful?, to check when Spark room is archived)
* add escalation process (button + extra contact/group list)
* add SMS notification (Twilio is ready, to check with Tropo)
* add bot for spec support

# Check list
## Web Form
[x] index (with dashboard)
[x] view - Space
[x] update - Space
[x] new - Space
[x] view - user
[x] update - user
[ ] new - user
[x]

## Web Feature
[x] user management (missing: user creation)
[x] folder management (new, update, delete) (missing: get Space files locally)
[x] folder closure only for admin role (missing: update in the local DB when Space is closed on Spark)
[x] folder dump (get Space content + local db) (missing: format output in PDF, CSV...)

## Cisco Spark
[x] creation (room, membership, message)
[x] messages webhook
[ ] rooms webhook (to get title and room events for local update)
[x] reading (message)
[x] dump (without attachment... for the moment)

## Local DB
[x] user & grp
[x] space lifecycle and events
[x] dump comes from local db
[x] log application
[x] evt storage
