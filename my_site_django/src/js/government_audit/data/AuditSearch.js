import Immutable from 'immutable';
import AuditDocument from './AuditDocument';
import NamedEntity from './NamedEntity';

function getWsScheme() {
    return window.location.protocol == "https:" ? "wss" : "ws";
}

function getVerifyUrlSocket() {
  if (typeof(WebSocket) !== "undefined") {
    return new WebSocket(getWsScheme() + "://" + window.location.host + "/verifyUrl")
  }
};

function getNamedEntitySearchSocket() {
  if (typeof(WebSocket) !== "undefined") {
    return new WebSocket(getWsScheme() + "://" + window.location.host + "/namedEntitySearch")
  }
};

const AuditSearch = Immutable.Record({
  query: '',
  queryParser: 'plain',
  years: Immutable.Set(['2017']),
  fetching: false,
  verifyUrlSocket: getVerifyUrlSocket(),
  namedEntitySocket: getNamedEntitySearchSocket(),
  namedEntity: NamedEntity(),
  auditDocument: AuditDocument(),
});

export default AuditSearch;
