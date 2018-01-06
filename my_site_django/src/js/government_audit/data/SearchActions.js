import Dispatcher from './Dispatcher';
import SearchActionTypes from './SearchActionTypes';

const SearchActions = {
  changeQuery(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.CHANGE_QUERY,
      event
    });
  },

  changeParser(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.CHANGE_PARSER,
      event
    });
  },

  changeYearSelection(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.CHANGE_YEAR_SELECTION,
      event
    });
  },

  submitQuery(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.SUBMIT_QUERY,
      event
    });
  },

  handleQueryResponse(response) {
    Dispatcher.dispatch({
      type: SearchActionTypes.LOAD_QUERY_RESPONSE,
      response
    });
  },

  changeDocumentPage(data) {
    Dispatcher.dispatch({
      type: SearchActionTypes.CHANGE_DOCUMENT_PAGE,
      data
    });
  },

  receiveUrlCheck(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.RECEIVE_URL_CHECK,
      event
    });
  },

  searchNamedEntity(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.SEARCH_NAMED_ENTITY,
      event
    });
  },

  changeEntityPage(data) {
    Dispatcher.dispatch({
      type: SearchActionTypes.CHANGE_ENTITY_PAGE,
      data
    });
  },

  receiveNamedEntityResults(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.RECEIVE_NAMED_ENTITY_RESULTS,
      event
    });
  },
};

export default SearchActions;
