import { Routes, Route } from 'react-router-dom';

import Home from './pages/home/home';
import Access from './pages/access/access';

export default function Router() {
  return (
    <Routes>
      <Route path="/" Component={Home} />
      <Route path="/access/:id" Component={Access}></Route>
    </Routes>
  );
}
