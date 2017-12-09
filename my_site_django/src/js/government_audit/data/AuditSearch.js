import Immutable from 'immutable';

function getWsScheme() {
    return window.location.protocol == "https:" ? "wss" : "ws";
}

function getVerifyUrlSocket() {
  if (typeof(WebSocket) !== "undefined") {
    return new WebSocket(getWsScheme() + "://" + window.location.host + "/verifyUrl")
  }
};

function getNamedEntitySocket() {
  if (typeof(WebSocket) !== "undefined") {
    return new WebSocket(getWsScheme() + "://" + window.location.host + "/namedEntity")
  }
};

const AuditSearch = Immutable.Record({
  query: '',
  queryParser: 'plain',
  years: Immutable.Set(['2017']),
  namedEntities: Immutable.List(),
  namedEntityResults: Immutable.List(),
  results: Immutable.List(),
  resultsOffset: 0,
  resultsLimit: 10,
  resultsSize: 0,
  verifyUrlSocket: getVerifyUrlSocket(),
  namedEntitySocket: getNamedEntitySocket(),
});

export default AuditSearch;
