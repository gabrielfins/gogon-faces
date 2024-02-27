import Navbar from './components/navbar/navbar';
import { AccessContextProvider } from './contexts/access-context';
import Router from './router';

export default function App() {
  return (
    <AccessContextProvider>
      <Navbar></Navbar>
      <Router />
    </AccessContextProvider>
  );
}
