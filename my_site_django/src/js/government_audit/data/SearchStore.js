import axios from 'axios';
import Immutable from 'immutable';
import {
  ReduceStore
} from 'flux/utils';
import Dispatcher from './Dispatcher';
import SearchActions from './SearchActions'
import SearchActionTypes from './SearchActionTypes';
import AuditSearch from './AuditSearch';


class AuditSearchStore extends ReduceStore {
  constructor() {
    super(Dispatcher);
  }

  getInitialState() {
    let auditSearch = new AuditSearch();

    auditSearch.verifyUrlSocket.onmessage = function(response) {
      SearchActions.receiveUrlCheck(response);
    };

    auditSearch.namedEntitySocket.onmessage = function(response) {
      SearchActions.receiveNamedEntityResults(response);
    };

    return auditSearch;
  }

  reduce(state, action) {
    switch (action.type) {
      case SearchActionTypes.CHANGE_QUERY:
        return state.set('query', action.event.target.value);

      case SearchActionTypes.CHANGE_PARSER:
        return state.set('queryParser', action.event.target.value);

      case SearchActionTypes.CHANGE_YEAR_SELECTION:
        {
          const toggledSelection = action.event.target.value;
          let updatedYears = state.years.includes(toggledSelection) ?
            state.years.delete(toggledSelection) : state.years.add(toggledSelection);

          return state.set('years', updatedYears);
        }

      case SearchActionTypes.SUBMIT_QUERY:
        if (action.event) {
          action.event.preventDefault();
        }

        if (state.query === '') {
          return state
        }

        state = state.set('resultsOffset', 0);

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
          state = state.set('results', state.results.set(result['id'], Object.assign(original, result)));
        }

        return state;
      }

      case SearchActionTypes.SEARCH_NAMED_ENTITY:
      {
        const target = action.event.target;

        if (target.id != "ne-exploration-heading") {
          state = state.set('namedEntities', state.namedEntities.push(target.innerText))
        }

        const message = JSON.stringify({
          'entityList': state.namedEntities,
          'years': state.years,
        });

        if (state.namedEntitySocket.readyState == WebSocket.OPEN) {
          state.namedEntitySocket.send(message);
        } else {
          console.log("NamedEntity Websocket is not open, cannot perform search.");
        }

        return state;
      }

      case SearchActionTypes.RECEIVE_NAMED_ENTITY_RESULTS:
      {
        action.event.preventDefault();

        const results = JSON.parse(action.event.data);

        state = state.set('namedEntityResults', Immutable.List(results['topEntities']));

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
        years: state.years,
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
