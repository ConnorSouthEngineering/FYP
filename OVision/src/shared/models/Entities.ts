import {v4 as uuid} from 'uuid';

export class Target {
    constructor(
        public name: string,
        public altName: string,
        public creationDate: Date,
        public status: 'Active' | 'Complete' | 'Expiring' | 'Error',
    ) {}
}

export class Person extends Target {
    public id: string;
    public dob: Date;
    public role: string;
    private age: number;

    constructor(name: string, altName: string, creationDate: Date, status: 'Active' | 'Complete' | 'Expiring' | 'Error', dob: Date, role: string) {
        super(name, altName, creationDate, status);
        this.id = 'P' + this.generateUniqueId();
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

    private generateUniqueId(): string {
        return uuid();
    }
}

export class Location extends Target {
    public id: string;
    public access: 'public' | 'private';

    constructor(name: string, altName: string, creationDate: Date, status: 'Active' | 'Complete' | 'Expiring' | 'Error', access: 'public' | 'private') {
        super(name, altName, creationDate, status);
        this.id = 'L' + this.generateUniqueId();
        this.access = access;
    }

    private generateUniqueId(): string {
        return uuid();
    }
}

export class Deployment {
    public id;
    constructor(
        public deploymentName: string,
        public targetID: string,
        public status: 'Active' | 'Complete' | 'Expiring' | 'Error',
        public runningTime: number,
        public modelID: string,
        public startDate: Date,
        public endDate: Date
    ) {
        this.id = 'D' + this.generateUniqueId();
    }

    private generateUniqueId(): string {
        return uuid();
    }
}

export class Report {
    public id;
    constructor(
        public reportName: string,
        public deploymentID: string,
        public frequency: number,
        public frequencyType: string,
        public lastGen: Date,
        public nextGen: Date
    ) {
        this.id = 'R' + this.generateUniqueId();
    }

    private generateUniqueId(): string {
        return uuid();
    }
}
