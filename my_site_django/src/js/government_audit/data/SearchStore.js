import axios from 'axios';
import Immutable from 'immutable';
import {
  ReduceStore
} from 'flux/utils';
import Dispatcher from './Dispatcher';
import SearchActions from './SearchActions'
import SearchActionTypes from './SearchActionTypes';
import SearchResults from './SearchResults';


class AuditSearchStore extends ReduceStore {
  constructor() {
    super(Dispatcher);
  }

  getInitialState() {
    let searchResults = new SearchResults();

    searchResults.verifyUrlSocket.onmessage = function(response) {
      SearchActions.receiveUrlCheck(response);
    };

    return searchResults;
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
        {
          const response = action.response.data;

          // Check the url of each result.  Can't do this browser side due to
          //  XSRF restrictions
          response.results.forEach(result => {
            const message = JSON.stringify({
              'id': result[0],
              'url': result[1]['url'],
            });

            if (state.verifyUrlSocket.readyState == WebSocket.OPEN) {
              state.verifyUrlSocket.send(message);
            } else {
              console.log("Websocket is not open, skipping URL checks");
            }
          });

          return state.merge({
            'results': Immutable.OrderedMap(response.results),
            'resultsSize': response.size,
            'resultsOffset': response.offset,
          });
        }

      case SearchActionTypes.CHANGE_PAGE:
        this.fetchResults(state.set('resultsOffset', Math.ceil(action.data.selected * state.resultsLimit)));
        return state; // original state without page changed.

      case SearchActionTypes.RECEIVE_URL_CHECK:
      {
        action.event.preventDefault();

        const result = JSON.parse(action.event.data);
        let original = state.results.get(result['id']);
        if (original) {
          // Must completely replace Immutable.Record
          state = new SearchResults(Object.assign(state.toJS(), {
            results: state.results.set(result['id'], Object.assign(original, result)),
          }));
        }

        return state;
      }

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
