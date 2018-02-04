import React from 'react';
import renderer from 'react-test-renderer';

import Immutable from 'immutable';
import AuditSearchView from '../views/AuditSearchView';
import AuditSearch from '../data/AuditSearch';

test('Default render', () => {
  const auditSearch = new AuditSearch();
  renderAndCheck(auditSearch);
});

test('Render with pagination visible (available result size > results per page limit)', () => {
   let auditSearch = AuditSearch();
   auditSearch = auditSearch.set('auditDocument',
    auditSearch.auditDocument.merge({
        results: Immutable.OrderedMap([
            ['1',
              { title: 'Ogglie Booglie',
                url: 'http://poundfoolish.com', // may be updated as part of url check (redirect occurred)
                date:'2012-2-13',
                rank: 0.1345, // Postgres measure of query match.  Results are returned in order of descending rank.
              }],
            [ '2',
              { title: 'Ogglie Booglie 2',
                url: 'http://poundfoolish2.com',
                date:'2013-2-13',
                rank: 0.14,
                url_active: true,
              }],
            [ '3',
              { title: 'Ogglie Booglie 3',
                url: 'http://poundfoolish3.com',
                date:'2014-2-13',
                rank: 0.15,
                url_active: false,
              }]]),
        resultsOffset: 0,
        resultsSize: 3,
        resultsLimit: 2,
        updatingPage: false,
      }));

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
