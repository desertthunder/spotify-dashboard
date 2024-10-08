import "./styles/base.css";
import "@fontsource-variable/inter";
import "@fontsource-variable/rubik";
import "@fontsource-variable/noto-sans-jp";
import { Query, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Signup, Dashboard } from "./pages";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";
import { persistQueryClient } from "@tanstack/react-query-persist-client";

// TODO: Move to libs
enum Routes {
  Home = "/",
  Signup = "/signup",
  Login = "/login",
  Dashboard = "/dashboard/",
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

const localStoragePersister = createSyncStoragePersister({
  storage: window.localStorage,
});

persistQueryClient({
  queryClient,
  persister: localStoragePersister,
  dehydrateOptions: {
    shouldDehydrateQuery(query: Query): boolean {
      // We're only persisting the token query
      // but also want to keep the default behavior.
      return query.queryKey[0] === "token" && query.state.status === "success";
    },
  },
});

export const BrowserRouter = createBrowserRouter([
  {
    // TODO: Add a home page
    path: Routes.Home,
    element: <Signup />,
  },
  {
    path: Routes.Login,
    element: <Signup />,
  },
  {
    path: Routes.Dashboard,
    element: <Dashboard />,
  },
]);

export default function Root() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={BrowserRouter} />
    </QueryClientProvider>
  );
}
