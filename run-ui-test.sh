DB_PATH="test_db.db"
export SQLITE_PATH="$DB_PATH"
export RELOAD_APP=False

poetry run python src/main.py &
APP_PID=$(echo $!)

cd src/tests/ui
npm ci
npm run mocha

cd ../../..
kill $APP_PID
sleep 1
rm $DB_PATH
unset SQLITE_PATH
unset RELOAD_APP
