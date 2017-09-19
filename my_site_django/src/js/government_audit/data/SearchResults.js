import Immutable from 'immutable';

function getWebSocket() {
  // TODO: This is a hack to get unit testing to work... fix and update the tests.
  if (typeof(WebSocket) !== "undefined") {
    return new WebSocket("ws://" + window.location.host + "/verifyUrl")
  }
};

const SearchResults = Immutable.Record({
  query: '',
  queryParser: 'plain',
  results: Immutable.List(),
  resultsOffset: 0,
  resultsLimit: 10,
  resultsSize: 0,
  verifyUrlSocket: getWebSocket(),
});


export default SearchResults;
