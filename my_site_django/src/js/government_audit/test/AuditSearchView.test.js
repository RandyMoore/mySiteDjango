import React from 'react';
import renderer from 'react-test-renderer';

import AuditSearchView from '../views/AuditSearchView';
import SearchResults from '../data/SearchResults';


test('Default render', () => {
  const searchResults = new SearchResults({
    'resultsSize': 0,
    'resultsLimit': 10
  });

  const component = renderer.create(
    <AuditSearchView
      searchResults={searchResults}
    />);

  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

test('Render with pagination visible', () => {
  const searchResults = new SearchResults({
    'resultsSize': 11,
    'resultsLimit': 10
  });

  const component = renderer.create(
    <AuditSearchView
      searchResults={searchResults}
    />);

  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});
