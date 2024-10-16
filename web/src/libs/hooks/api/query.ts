/**
 * @todo paginate queries
 */
import {
  FetchError,
  LibraryCountsResponse,
  Resource,
  ResourceKey,
  BrowserPlaylistResponse,
} from "@/libs/types";
import {
  useQuery,
  useQueryClient,
  UseQueryResult,
} from "@tanstack/react-query";
import { useEffect } from "react";
import { useSearch } from "wouter";
import { browserFetcher, fetcher, paginatedBrowserFetcher } from "./fetch";
import { BASE_URL } from "@/libs/services";
import { useTokenStore } from "@/store";

export function useQueryParams(): Record<string, string> {
  const [search] = useSearch();
  const params = new URLSearchParams(search);

  return Object.fromEntries(params.entries());
}

export function useTokenValidator() {
  const params = useQueryParams();
  const queryClient = useQueryClient();
  const token = useTokenStore((state) => state.token);
  const setToken = useTokenStore((state) => state.setToken);

  useEffect(() => {
    if (params.token) {
      setToken(params.token);
    }
  }, [params.token, setToken]);

  const query = useQuery(
    {
      queryKey: ["token"],
      queryFn: async () => {
        console.debug("Checking token validity");

        if (!token) {
          throw new Error("Token not found");
        }

        const response = await fetch("/api/validate", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Token invalid");
        }

        const data: { message: string; token: string } = await response.json();

        return data;
      },
      retry: false,
      refetchInterval: 5 * 60 * 1000, // 5 minutes
    },
    queryClient
  );

  return query;
}

export function useFetch<T extends ResourceKey>(
  resource: ResourceKey,
  limit?: number | null
): UseQueryResult<Resource<T>> {
  const token = useTokenStore((state) => state.token);
  const client = useQueryClient();

  const query = useQuery<Resource<T>>(
    {
      queryKey: [resource],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        return await fetcher<T>(resource, token, limit);
      },
    },
    client
  );

  return query;
}

export function useBrowse<T extends ResourceKey>(
  resource: T
): UseQueryResult<Resource<T>> {
  const token = useTokenStore((state) => state.token);
  const client = useQueryClient();

  const query = useQuery<Resource<T>>(
    {
      queryKey: [`${resource}-browser`],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        return await browserFetcher<T>(resource, token);
      },
    },
    client
  );

  return query;
}

export function useSavedCounts() {
  const token = useTokenStore((state) => state.token);
  const client = useQueryClient();

  const query = useQuery(
    {
      queryKey: ["saved-counts"],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        const response = await fetch(`${BASE_URL}/api/data/saved`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          return Promise.reject({
            code: response.status,
            message: response.statusText,
          } as FetchError);
        }

        const data = (await response.json()) as LibraryCountsResponse;

        return data["data"];
      },
    },
    client
  );

  return query;
}

export function usePlaylistTracks(id: string) {
  const token = useTokenStore((state) => state.token);
  const client = useQueryClient();
  const query = useQuery(
    {
      queryKey: ["playlist", id],
      queryFn: async () => {
        const response = await fetch(`/api/browser/playlist/${id}/tracks`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch playlist tracks");
        }

        return (await response.json()) as BrowserPlaylistResponse;
      },
    },
    client
  );

  return query;
}

export function usePaginatedBrowser<T extends ResourceKey>(
  resource: T,
  params: {
    page: number;
    page_size: number;
  } = {
    page: 1,
    page_size: 10,
  }
): UseQueryResult<Resource<T>> {
  const token = useTokenStore((state) => state.token);
  const client = useQueryClient();

  const query = useQuery<Resource<T>>(
    {
      queryKey: [`${resource}`],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        return await paginatedBrowserFetcher<T>(resource, token, params);
      },
    },
    client
  );

  return query;
}
