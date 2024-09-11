export interface ICarProfileModel {
    id: number
    city: string,
    region: string,
    description: string,
    color: string,
    owner_number: number,
    mileage: number,
    engine: string,
    engine_capacity: number,
    transmission: string,
    body: string,
    photo: string,
    created_at: Date,
    updated_at: Date,
}