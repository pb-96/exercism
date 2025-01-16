use knapsack::*;

pub fn main() {
    let max_weight = 10;
    let items: [Item; 5] = [
        Item {
            weight: 2,
            value: 5,
        },
        Item {
            weight: 2,
            value: 5,
        },
        Item {
            weight: 2,
            value: 5,
        },
        Item {
            weight: 2,
            value: 5,
        },
        Item {
            weight: 10,
            value: 21,
        },
    ];
    let value: u32 = maximum_value(max_weight, &items);
    println!("{:?}", value);

}