function run_minimal() {
  URL="http://127.0.0.1:8000/hello/minimal"
  http $URL
  time wrk -t20 -c50 -d10s $URL
}

function run_parameter() {
  URL="http://127.0.0.1:8000/hello/with/foobar"
  http $URL
  time wrk -t20 -c50 -d10s $URL
}

function run_cookie() {
  URL="http://127.0.0.1:8000/hello/cookie"
  http $URL Cookie:"test=bench"
  time wrk -t20 -c50 -d10s -H "Cookie: test=bench" $URL
}

function run_query() {
  URL="http://127.0.0.1:8000/hello/query?query=foobar"
  http $URL
  time wrk -t20 -c50 -d10s $URL
}

function run_full() {
  URL="http://127.0.0.1:8000/hello/full/with/foo/and/bar?query=foobar"
  http $URL Cookie:"test=bench"
  time wrk -t20 -c50 -d10s -H "Cookie: test=bench" $URL
}


echo "Running bench for Horseman Sample."
python bench.py &
sleep 1
PID=$!
run_minimal
run_parameter
run_cookie
run_query
run_full
kill $PID
wait $PID
