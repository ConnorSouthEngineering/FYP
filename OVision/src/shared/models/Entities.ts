import {v4 as uuid} from 'uuid';

export class Target {
    constructor(
        public target_name: string,
        public alt_name: string,
        public creation_date: Date,
        public status_value: 'Active' | 'Complete' | 'Expiring' | 'Error',
    ) {}
}

export class Person extends Target {
    public dob: Date;
    public role: string;
    public age: number;

    constructor(
        public target_id:string, 
        target_name: string, 
        alt_name: string, 
        creation_date: Date, 
        status_value: 'Active' | 'Complete' | 'Expiring' | 'Error', 
        dob: Date, 
        role: string) 
        {
        super(target_name, alt_name, creation_date, status_value);
        this.dob = dob;
        this.role = role;
        this.age = this.getAge(dob);
    }

    private getAge(dob: Date): number {
        const today = new Date();
        const age = today.getFullYear() - dob.getFullYear();
        const month = today.getMonth() - dob.getMonth();
        if (month < 0 || (month === 0 && today.getDate() < dob.getDate())) {
            return age - 1;
        }
        return age;
    }

/*     private generateUniqueId(): string {
        return uuid();
    } */
}

export class Location extends Target {
    constructor(
        public target_id:string,
        target_name: string,
        alt_name: string,
        creation_date: Date,
        status_value: 'Active' | 'Complete' | 'Expiring' | 'Error',
        public access: 'public' | 'private') 
        {
        super(target_name, alt_name, creation_date, status_value);
    }
}

export class Deployment {
    constructor(
        public deployment_id: string,
        public deployment_name: string,
        public target_id: string,
        public status_value: 'Active' | 'Complete' | 'Expiring' | 'Error',
        public running_time: number,
        public model_id: string,
        public start_date: Date,
        public end_date: Date
    ){}
}

export class Report {
    constructor(
        public report_id: string,
        public report_name: string,
        public deployment_id: string,
        public frequency: number,
        public frequency_type: string,
        public last_gen: Date,
        public next_gen: Date,
        public graph_type: string,
        public activity_set: Array<string>
    ){}
}
