import React from 'react';
import renderer from 'react-test-renderer';

import Immutable from 'immutable';
import AuditSearchView from '../views/AuditSearchView';
import AuditSearch from '../data/AuditSearch';

// What data may look like after query fetch
const baseAuditSearch = {
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
  const auditSearch = new AuditSearch(Object.assign({}, baseAuditSearch,
    {results: new Immutable.OrderedMap()}));

  renderAndCheck(auditSearch);
});

test('Render with pagination visible (available result size > results per page limit)', () => {
  const auditSearch = new AuditSearch(Object.assign({}, baseAuditSearch,
    { 'resultsSize': 11 }));

  // Note in real life the table would have resultsLimit rows intsead of 1.
  renderAndCheck(auditSearch);
});

test('Render result before URL validity check', () => {
  const auditSearch = new AuditSearch(baseAuditSearch);

  // CSS on result row title will be italic.
  renderAndCheck(auditSearch);
});

test('Render result after URL validity check returns active', () => {
  // Add isActive: true to result object with key 1
  const activeResult = new Immutable.OrderedMap( [['1', Object.assign({},
    baseAuditSearch.results.get('1'),
    {isActive: true})]]);
  const auditSearch = new AuditSearch(Object.assign({}, baseAuditSearch,
    { 'results': activeResult }));

  // CSS on result row title will be blue #0000FF and normal
  renderAndCheck(auditSearch);
});

test('Render result after URL validity check returns not active', () => {
  // Add isActive: false to result object with key 1
  const inActiveResult = new Immutable.OrderedMap( [['1', Object.assign({},
    baseAuditSearch.results.get('1'),
    {isActive: false})]]);
  const auditSearch = new AuditSearch(Object.assign({}, baseAuditSearch,
    { 'results': inActiveResult }));

  // CSS on result row title will be red #FF0000 and strike through
  renderAndCheck(auditSearch);
});

// Helper functions
function renderAndCheck(auditSearch) {
  const component = renderer.create(
    <AuditSearchView
      auditSearch={auditSearch}
    />);

  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
}
