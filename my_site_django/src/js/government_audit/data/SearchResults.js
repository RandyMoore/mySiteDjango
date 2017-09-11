import Immutable from 'immutable';

const SearchResults = Immutable.Record({
  query: '',
  queryParser: 'plain',
  results: Immutable.List(),
  resultsOffset: 0,
  resultsLimit: 10,
  resultsSize: 0,
});

export default SearchResults;
