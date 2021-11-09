/* eslint-disable jsx-a11y/anchor-is-valid */
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './components/Home';
import NotFound from './components/layout/NotFound';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path='/' component={Home} />
        <Route exact path='/home' component={Home} />
        <Route component={NotFound} />
      </Switch>
    </Router>
  );
}

export default App;
