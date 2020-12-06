defmodule Math do
  def zero?(0), do: true
  def zero?(x) when is_integer(x), do: false
end

defmodule BoardingPass do
  IO.puts("Day 5 in elixir")

  defp convert_to_bits(letter) do
    case letter do
      "F" -> <<0::1>>
      "L" -> <<0::1>>
      "B" -> <<1::1>>
      "R" -> <<1::1>>
    end
  end

  def join_bits(x, y) do
    <<x::bitstring, y::bitstring>>
  end

  def get_bits(input) do
    input
    |> String.graphemes()
    |> Enum.map(&convert_to_bits/1)
    |> Enum.reduce(<<>>, &join_bits/2)
  end

  def get_seat_from_row_col(row, col) do
    row * 8 + col
  end

  def get_seat(x) do
    # x = "FBFBBFFRLR"
    <<column::bytes-size(3), row::bytes-size(7)>> = x |> String.reverse()
    # IO.puts("Split into row: #{row} and column: #{column}")
    bit_string_rows = get_bits(row)
    bit_string_column = get_bits(column)
    <<row_number::integer-size(7)>> = bit_string_rows
    <<column_number::integer-size(3)>> = bit_string_column
    # IO.puts("row is #{row_number}, column is #{column_number}")
    get_seat_from_row_col(row_number, column_number)
  end
end

{:ok, boarding_passes_raw_sample} = File.read("day_five_data_sample.txt")
{:ok, boarding_passes_raw} = File.read("day_five_data.txt")

max_seat_id =
  boarding_passes_raw
  |> String.split("\n")
  |> Enum.map(&BoardingPass.get_seat/1)
  |> Enum.max()

IO.puts("The max seat id is #{max_seat_id}")

defmodule SeatFinder do
  def find([head | tail]) do
    # IO.puts(head)
    # IO.puts(tail)
    cond do
      head + 1 == List.first(tail) -> find(tail)
      true -> head + 1
    end
  end
end

l = [1, 2, 3, 4, 6, 7, 8]

seats =
  boarding_passes_raw
  |> String.split("\n")
  |> Enum.map(&BoardingPass.get_seat/1)
  |> Enum.sort()

# could just look at the seats
# IO.inspect seats, charlists: :as_lists

my_seat = SeatFinder.find(seats)
IO.puts("My seat is id: #{my_seat}")
