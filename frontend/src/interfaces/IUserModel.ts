import {IProfileModel} from "./IProfileModel";

export interface IUserModel {
    id: number,
    email: string,
    password: string,
    is_active: boolean,
    is_premium: boolean,
    is_staff: boolean,
    is_superuser: boolean,
    last_login: Date | null,
    created_at: Date,
    updated_at: Date,
    profile: IProfileModel,
    dealership_id: number,
}