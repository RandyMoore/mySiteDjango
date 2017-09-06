import React from 'react';
import AuditSearch from '../audit_search.react.js';
import renderer from 'react-test-renderer';

test('Default render', () => {
  const component = renderer.create(
    <AuditSearch />);

  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

test('Render with supplied props', () => {
  const component = renderer.create(
    <AuditSearch
      query='Ooglie booglie'
      pageCount={3}
      resultsOffset={10}
     />);

  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});
