import Immutable from 'immutable';

const AuditDocument = Immutable.Record({
    results: Immutable.OrderedMap(),
    resultsOffset: 0,
    resultsSize: 0,
    resultsLimit: 10,
    updatingPage: false,
});

export default AuditDocument
