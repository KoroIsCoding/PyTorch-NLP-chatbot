from models import SearchEngineStruct


se = SearchEngineStruct()
assert se.google_api_key == 'AIzaSyAGHYwrgMmAHlFwM-GmS2anQ7xWu7qcIjA'
assert se.google_engine_key == '7a8bd65adc0b760d8'
assert se.top_result == list()
seed_query = 'per se'
se.set_query(seed_query)
se.call_google_custom_search_api()

se.choose_relevant()
print(se.query)
se.add_and_reorder_words()
print(se.query)
