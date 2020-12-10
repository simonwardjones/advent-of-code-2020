

def load_data
    day_three_data_filename = 'day_three_data.txt'
    day_three_data_path = File.join(__dir__, day_three_data_filename)
    data =  File.readlines(day_three_data_path).map do |line|
        # puts line
        line.strip().split('').map do |val|
            val == '#'
        end
    end
    return data
end

def find_counts (step_right, step_down)
    data = load_data
    n_rows = data.length
    n_cols = data[0].length
    # p "#{n_rows} n_rows by n_cols #{n_cols}"
    pos = [0,0]
    tree_count = data[0][0] ? 1 : 0

    while pos[0] + step_down < n_rows
        pos[0] += step_down
        pos[1] += step_right
        pos[1] = pos[1].modulo n_cols # incase we have walked off
        tree_count = data[pos[0]][pos[1]] ? tree_count + 1 : tree_count
        # p pos, tree_count
    end
    # puts tree_count
    return tree_count
end

# find_counts 3, 1

def part_two
    settings = [[1, 1],[3, 1],[5, 1],[7, 1],[1,2]]
    values = settings.map do |right , down|
        find_counts right, down
    end
    result = 1
    values.each do |val|
        result *= val
    end
    p values
    p result

end

part_two