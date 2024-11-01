import {
  useReactTable,
  createColumnHelper,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";
import { useQuery } from "@tanstack/react-query";
import { useTokenStore } from "@/store";
import { Menu } from "./menu";
import { usePlaylistFilters } from "./filters/store";
import { useEffect, useMemo } from "react";
/**
 * {"json":{"is_synced":true,"is_analyzed":true,"description":"With Brian McBride, The Dead Texan, William Basinski and more","owner_id":"spotify","version":"ZyPYkgAAAACmpgMNhm9gMhsvWVQyX5cB","image_url":"https://pickasso.spotifycdn.com/image/ab67c0de0000deef/dt/v1/img/radio/artist/36pCa1JHc6hlGbfEmLzJQc/en","public":true,"shared":false,"id":"88a0fa4f-f2eb-46e6-9731-f4b289b4fe62","name":"Stars Of The Lid Radio","spotify_id":"37i9dQZF1E4pndHPIu7Fgn"}}
 */
type BrowserPlaylist = {
  is_synced: boolean;
  is_analyzed: boolean;
  description: string;
  owner_id: string;
  version: string;
  image_url: string;
  public: boolean;
  shared: boolean;
  id: string;
  name: string;
  spotify_id: string;
};

const columnHelper = createColumnHelper<BrowserPlaylist>();

const columns = [
  columnHelper.accessor("id", {
    header: () => null,
    cell: () => (
      <form className="flex justify-center w-16 text-center">
        <input type="checkbox" />
      </form>
    ),
  }),
  columnHelper.accessor("image_url", {
    header: () => null,
    cell: (props) => (
      <p className="min-w-8">
        <img src={props.getValue()} className="w-16" alt="Playlist Image" />
      </p>
    ),
  }),
  columnHelper.accessor("name", {
    header: "Name",
  }),
  columnHelper.accessor("description", {
    header: () => (
      <>
        <span className="hidden lg:inline">Description</span>
        <span className="lg:hidden">Desc.</span>
      </>
    ),
    cell: (props) => (
      <p className="max-w-64 truncate">
        {props.getValue() ? (
          props.getValue()
        ) : (
          <span className="text-gray-500 italic">None</span>
        )}
      </p>
    ),
  }),
  columnHelper.accessor("owner_id", {
    header: "Owner",
  }),
  columnHelper.accessor("public", {
    header: "Public",
    cell: (props) => {
      return (
        <span className={props.getValue() ? "text-green-500" : "text-red-500"}>
          {props.getValue() ? "Yes" : "No"}
        </span>
      );
    },
  }),
  columnHelper.accessor("shared", {
    header: "Shared",
    cell: (props) => {
      return (
        <span className={props.getValue() ? "text-green-500" : "text-red-500"}>
          {props.getValue() ? "Yes" : "No"}
        </span>
      );
    },
  }),
  columnHelper.accessor("is_analyzed", {
    header: () => {
      return (
        <>
          <span className="hidden lg:inline">Analyzed</span>
          <i className="lg:hidden i-ri-line-chart-line" />
        </>
      );
    },
    cell: (props) => {
      return (
        <span className={props.getValue() ? "text-green-500" : "text-red-500"}>
          {props.getValue() ? "Yes" : "No"}
        </span>
      );
    },
  }),
  columnHelper.display({
    header: "Actions",
    cell: () => <Menu />,
  }),
  columnHelper.accessor("spotify_id", {
    header: "Link",
    cell: (props) => {
      const link = `https://open.spotify.com/playlist/${props.getValue()}`;
      return (
        <a href={link} target="_blank" rel="noreferrer">
          Open
        </a>
      );
    },
  }),
];

async function fetchPlaylists(token: string | null, params: URLSearchParams) {
  const uri = new URL("/api/v1/browser/playlists", window.location.origin);
  uri.search = params.toString();
  const response = await fetch(uri.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch playlists");
  }

  return (await response.json()) as {
    data: BrowserPlaylist[];
    pagination: {
      total: number;
      per_page: number;
      page: number;
      num_pages: number;
    };
  };
}

export function Table() {
  const token = useTokenStore((state) => state.token);
  const updateTotal = usePlaylistFilters((state) => state.updateTotal);
  const page = usePlaylistFilters((state) => state.page);
  const pageSize = usePlaylistFilters((state) => state.pageSize);
  const updateFetching = usePlaylistFilters((state) => state.updateFetching);

  const params = useMemo(() => {
    const params = new URLSearchParams();
    params.set("page", page.toString());
    params.set("page_size", pageSize.toString());
    return params;
  }, [page, pageSize]);

  const query = useQuery({
    queryKey: ["browser", "playlists", params.toString()],
    queryFn: async () => {
      const data = await fetchPlaylists(token, params);

      updateTotal(data.pagination.total);

      return data;
    },
  });

  const table = useReactTable({
    columns,
    data: query.data?.data || [],
    getCoreRowModel: getCoreRowModel(),
  });

  if (query.data?.pagination) {
    updateTotal(query.data.pagination.total);
  }

  useEffect(() => {
    const isFetching = query.isLoading || query.isFetching || query.isFetching;

    updateFetching(isFetching);
  }, [query.isLoading, query.isFetching, updateFetching]);

  return (
    <table className="table-fixed lg:table-auto w-full border-collapse">
      <thead className="font-sans text-base text-left bg-emerald-500 text-zinc-50">
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th
                key={header.id}
                className={[
                  "p-2",
                  "font-semibold",
                  "border-r border-slate-200 last:border-none",
                ].join(" ")}
              >
                {header.isPlaceholder
                  ? null
                  : flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {query.isLoading ? (
          <tr className="bg-zinc-50 even:bg-green-200 text-xs">
            <td colSpan={columns.length} className="text-center text-3xl p-12">
              <i className="i-ri-loader-line animate-spin" />
            </td>
          </tr>
        ) : query.isError ? (
          <tr className="bg-zinc-50 even:bg-green-200 text-xs text-red-500">
            <td colSpan={columns.length} className="px-4">
              Unable to fetch playlists: {query.error.message}
            </td>
          </tr>
        ) : (
          table.getRowModel().rows.map((row) => (
            <tr key={row.id} className="bg-zinc-50 even:bg-green-200 text-xs">
              {row.getVisibleCells().map((cell) => (
                <td
                  key={cell.id}
                  className={[
                    "border-r border-slate-300 last:border-none px-2",
                  ].join(" ")}
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))
        )}
      </tbody>
    </table>
  );
}