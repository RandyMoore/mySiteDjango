import Immutable from 'immutable';
import AuditDocument from './AuditDocument';
import NamedEntity from './NamedEntity';

function getWsScheme() {
    return window.location.protocol == "https:" ? "wss" : "ws";
}

function getNamedEntitySearchSocket() {
  if (typeof(WebSocket) !== "undefined") {
    return new WebSocket(getWsScheme() + "://" + window.location.host + "/ws/namedEntitySearch")
  }
};

const AuditSearch = Immutable.Record({
  query: '',
  queryParser: 'plain',
  years: Immutable.Set(['2017']),
  fetching: false,
  namedEntitySocket: getNamedEntitySearchSocket(),
  namedEntity: NamedEntity(),
  auditDocument: AuditDocument(),
});

export default AuditSearch;
