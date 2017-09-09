import axios from 'axios'
import {ReduceStore} from 'flux/utils';
import Immutable from 'immutable';
import Dispatcher from './Dispatcher';
import SearchActions from './SearchActions'
import SearchActionTypes from './SearchActionTypes';
import SearchResults from './SearchResults';


class AuditSearchStore extends ReduceStore {
  constructor() {
    super(Dispatcher);
  }

  getInitialState() {
    return new SearchResults();
  }

  reduce(state, action) {
    switch (action.type) {
      case SearchActionTypes.CHANGE_QUERY:
        return state.set('query', action.event.target.value);

      case SearchActionTypes.CHANGE_PARSER:
        return state.set('queryParser', action.event.target.value);

      case SearchActionTypes.SUBMIT_QUERY:
        if (action.event) {
          action.event.preventDefault();
        }

        if (state.query === '') {
            return state
        }

        this.fetchResults(state);

        return state;

      case SearchActionTypes.LOAD_QUERY_RESPONSE:
        const response = action.response.data;
        return state.merge({
          'results': response.results,
          'resultsSize': response.size,
          'resultsOffset': response.offset,
        });

      case SearchActionTypes.CHANGE_PAGE:
        this.fetchResults(state.set('resultsOffset', Math.ceil(action.data.selected * state.resultsLimit)));
        return state // original state without page changed.

      default:
        return state;
    }
  }

// Helper functions
  fetchResults(state) {
    axios.get('/audits/search/', {
      params: {
        query: state.query,
        parser: state.queryParser,
        limit: state.resultsLimit,
        offset: state.resultsOffset
      }
    }).then(res => {
      SearchActions.handleQueryResponse(res);
    });
  }
}

export default new AuditSearchStore();
