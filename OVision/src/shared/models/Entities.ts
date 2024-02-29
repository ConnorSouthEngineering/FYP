export class Target {
    constructor(
        public target_id:number, 
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
        target_id:number, 
        target_name: string, 
        alt_name: string, 
        creation_date: Date, 
        status_value: 'Active' | 'Complete' | 'Expiring' | 'Error', 
        dob: Date, 
        role: string) 
        {
        super(target_id, target_name, alt_name, creation_date, status_value);
        this.dob = dob;
        this.role = role;
        this.age = this.getAge(dob);
    }

    public getAge(dob: Date): number {
        const today = new Date();
        const age = today.getFullYear() - dob.getFullYear();
        const month = today.getMonth() - dob.getMonth();
        if (month < 0 || (month === 0 && today.getDate() < dob.getDate())) {
            return age - 1;
        }
        return age;
    }

}

export class Location extends Target {
    constructor(
        target_id:number,
        target_name: string,
        alt_name: string,
        creation_date: Date,
        status_value: 'Active' | 'Complete' | 'Expiring' | 'Error',
        public access: 'public' | 'private') 
        {
        super(target_id,target_name, alt_name, creation_date, status_value);
    }
}

export class Deployment {
    constructor(
        public deployment_id: string,
        public deployment_name: string,
        public target_id: string,
        public status_value: 'Active' | 'Complete' | 'Expiring' | 'Error',
        public model_id: string,
        public creation_date: Date,
        public start_date: Date,
        public expiry_date: Date
    ){}

    get running_time(): number {
        const currentDate = new Date();
        const startDateMidnight = new Date(this.start_date);
        startDateMidnight.setHours(0, 0, 0, 0); 
        const timeDiff = currentDate.getTime() - startDateMidnight.getTime();
        const hoursDiff = timeDiff / (1000 * 3600); 
        return Math.floor(hoursDiff); 
    }
}

export class Report {
    constructor(
        public report_id: string,
        public report_name: string,
        public deployment_id: string,
        public frequency_value: number,
        public frequency_unit: string,
        public creation_date: Date,
        public last_gen: Date | null,
        public graph_id: string,
    ) {}

    public calculateNextGen(): Date {
        let baseDate = this.last_gen ? new Date(this.last_gen) : new Date(this.creation_date);

        switch (this.frequency_unit) {
            case 'day':
                baseDate.setDate(baseDate.getDate() + this.frequency_value);
                break;
            case 'week':
                baseDate.setDate(baseDate.getDate() + (this.frequency_value * 7));
                break;
            case 'month':
                baseDate.setMonth(baseDate.getMonth() + this.frequency_value);
                break;
            case 'year':
                baseDate.setFullYear(baseDate.getFullYear() + this.frequency_value);
                break;
            default:
                throw new Error('Unsupported frequency unit');
        }
        return new Date(baseDate);
    }
}
