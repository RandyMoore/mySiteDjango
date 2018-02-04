import axios from 'axios';
import Immutable from 'immutable';
import {ReduceStore} from 'flux/utils';
import Dispatcher from './Dispatcher';
import SearchActions from './SearchActions'
import SearchActionTypes from './SearchActionTypes';
import AuditSearch from './AuditSearch';
import NamedEntity from './NamedEntity';


class AuditSearchStore extends ReduceStore {
  constructor() {
    super(Dispatcher);
  }

  getInitialState() {
    let auditSearch = new AuditSearch();

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

        state = state.set('namedEntity', state.namedEntity.merge({
          selectedEntities: Immutable.List(),
          results: Immutable.List(),
          resultsSize: 0,
          resultsOffset: 0,
        }));

        state = state.set('auditDocument', state.auditDocument.merge({
           results: Immutable.List(),
           resultsSize: 0,
           resultsOffset: 0,
        }));

        this.fetchResults(state);

        state = state.set('fetching', true);

        return state;

      case SearchActionTypes.LOAD_QUERY_RESPONSE:
        {
          const response = action.response.data;

          state = state.set('auditDocument', state.auditDocument.merge({
            results: Immutable.OrderedMap(response.documentResults),
            resultsSize: response.documentResultsSize,
            resultsOffset: response.documentOffset,
          }));

          state = state.set('fetching', false);
          state = state.setIn(['auditDocument', 'updatingPage'], false);

          return state;
        }

      case SearchActionTypes.CHANGE_DOCUMENT_PAGE:
        {
          const offset = Math.ceil(action.data.selected * state.auditDocument.resultsLimit);
          if (state.query != '') {
            this.fetchResults(state.setIn(['auditDocument', 'resultsOffset'], offset));
          } else {
            const message = JSON.stringify({
              'selectedEntities': state.namedEntity.selectedEntities,
              'entityOffset': state.namedEntity.resultsOffset,
              'years': state.years,
              'documentOffset': offset
            });

            this.namedEntitySearch(state, message);
          }

          state = state.setIn(['auditDocument', 'updatingPage'], true);

          return state; // original state without page changed.
        }

      case SearchActionTypes.SEARCH_NAMED_ENTITY:
      {
        let selectedEntities = state.namedEntity.selectedEntities.toJS();
        selectedEntities.push(action.event.target.innerText);

        const message = JSON.stringify({
          'selectedEntities': selectedEntities,
          'entityOffset': 0,
          'years': state.years,
          'documentOffset': 0,
        });

        this.namedEntitySearch(state, message);

        state = state.set('fetching', true);

        return state;
      }

      case SearchActionTypes.RECEIVE_NAMED_ENTITY_RESULTS:
      {
        action.event.preventDefault();

        const response = JSON.parse(action.event.data);

        state = state.merge({
          query: '',
        });

        state = state.set('namedEntity', state.namedEntity.merge({
          results: Immutable.fromJS(response['topEntities']),
          resultsSize: response.entityResultsSize,
          resultsOffset: response.entityOffset,
          selectedEntities: Immutable.fromJS(response['selectedEntities']),
        }));

        state = state.set('auditDocument', state.auditDocument.merge({
          results: Immutable.OrderedMap(response.documentResults),
          resultsSize: response.documentResultsSize,
          resultsOffset: response.documentOffset,
        }));

        state = state.set('fetching', false);
        state = state.setIn(['namedEntity', 'updatingPage'], false);
        state = state.setIn(['auditDocument', 'updatingPage'], false);

        return state;
      }

      case SearchActionTypes.CHANGE_ENTITY_PAGE:
        {
          const selected_page = action.data.selected;
          const entityOffset = selected_page
            ? Math.ceil(selected_page * state.namedEntity.resultsLimit)
            : 0;
          const namedEntities = state.namedEntity.selectedEntities.toJS();

          const message = JSON.stringify({
            'selectedEntities': namedEntities,
            'years': state.years,
            'entityOffset': entityOffset,
            'documentOffset': state.auditDocument.resultsOffset
          });

          this.namedEntitySearch(state, message);

          state = state.setIn(['namedEntity', 'updatingPage'], true);

          return state; // original state without page changed.
        }

      default:
        return state;
    }
  }

  fetchResults(state) {
    axios.get('/audits/search/', {
      params: {
        query: state.query,
        years: state.years,
        parser: state.queryParser,
        limit: state.auditDocument.resultsLimit,
        offset: state.auditDocument.resultsOffset
      }
    }).then(res => {
      SearchActions.handleQueryResponse(res);
    });
  };

  namedEntitySearch(state, searchMessage) {
    if (state.namedEntitySocket.readyState == WebSocket.OPEN) {
      state.namedEntitySocket.send(searchMessage);
    } else {
      console.log("namedEntitySearch Websocket is not open, cannot perform search.");
    }
  };
}

export default new AuditSearchStore();
