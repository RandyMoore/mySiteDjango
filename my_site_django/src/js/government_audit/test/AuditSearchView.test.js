import React from 'react';
import renderer from 'react-test-renderer';

import Immutable from 'immutable';
import AuditSearchView from '../views/AuditSearchView';
import SearchResults from '../data/SearchResults';

// What data may look like after query fetch
const baseSearchResults = {
  resultsSize: 1,
  resultsLimit: 10,
  results: new Immutable.OrderedMap([['1',  // '1' would be DB primary key
    { title: 'Ogglie Booglie',
      url: 'http://poundfoolish.com', // may be updated as part of url check (redirect occurred)
      date:'2012-2-13',
      rank: 0.1345, // Postgres measure of query match.  Results are returned in order of descending rank.
      // isActive: [true|false] will be added after url check.
    }]])};


test('Default render', () => {
  const searchResults = new SearchResults(Object.assign({}, baseSearchResults,
    {results: new Immutable.OrderedMap()}));

  renderAndCheck(searchResults);
});

test('Render with pagination visible (available result size > results per page limit)', () => {
  const searchResults = new SearchResults(Object.assign({}, baseSearchResults,
    { 'resultsSize': 11 }));

  // Note in real life the table would have resultsLimit rows intsead of 1.
  renderAndCheck(searchResults);
});

test('Render result before URL validity check', () => {
  const searchResults = new SearchResults(baseSearchResults);

  // CSS on result row title will be italic.
  renderAndCheck(searchResults);
});

test('Render result after URL validity check returns active', () => {
  // Add isActive: true to result object with key 1
  const activeResult = new Immutable.OrderedMap( [['1', Object.assign({},
    baseSearchResults.results.get('1'),
    {isActive: true})]]);
  const searchResults = new SearchResults(Object.assign({}, baseSearchResults,
    { 'results': activeResult }));

  // CSS on result row title will be blue #0000FF and normal
  renderAndCheck(searchResults);
});

test('Render result after URL validity check returns not active', () => {
  // Add isActive: false to result object with key 1
  const inActiveResult = new Immutable.OrderedMap( [['1', Object.assign({},
    baseSearchResults.results.get('1'),
    {isActive: false})]]);
  const searchResults = new SearchResults(Object.assign({}, baseSearchResults,
    { 'results': inActiveResult }));

  // CSS on result row title will be red #FF0000 and strike through
  renderAndCheck(searchResults);
});

// Helper functions
function renderAndCheck(searchResults) {
  const component = renderer.create(
    <AuditSearchView
      searchResults={searchResults}
    />);

  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
}
