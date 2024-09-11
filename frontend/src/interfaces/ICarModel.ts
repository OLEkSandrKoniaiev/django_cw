import {IUserModel} from "./IUserModel";
import {IModelModel} from "./IModelModel";

export interface ICarModel {
    id: number,
    model: IModelModel,
    year: number,
    price: number,
    currency: string,
    is_new: boolean,
    is_active: boolean,
    edit_attempts: number,
    user: IUserModel,
    created_at: Date,
    updated_at: Date,
}