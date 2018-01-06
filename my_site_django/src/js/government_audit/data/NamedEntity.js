import Immutable from 'immutable';

const NamedEntity = Immutable.Record({
    selectedEntities: Immutable.List(),
    results: Immutable.List(),
    resultsOffset: 0,
    resultsSize: 0,
    resultsLimit: 10,
    updatingPage: false,
});

export default NamedEntity;
