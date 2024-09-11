import {IBrandModel} from "./IBrandModel";

export interface IModelModel {
    id: number,
    brand: IBrandModel,
    name: string,
    created_at: Date,
    updated_at: Date,
}