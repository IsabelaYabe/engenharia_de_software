class DatabaseManagerClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async getRecordById(recordType, recordId) {
        try {
            const response = await fetch(`${this.baseUrl}/api/${recordType}/${recordId}`);
            if (!response.ok) {
                throw new Error(`Error: ${response.status} - ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Failed to fetch record:", error);
            return null;
        }
    }

    async loadItemDetails(recordType, recordId, itemDetails) {
        const record = await this.getRecordById(recordType, recordId);
        if (record) {
            for (const detail of itemDetails) {
                const element = document.querySelector(`.${detail}`);
                if (element) {
                    element.textContent = record[detail];
                } else {
                    console.warn(`Element with class '.${detail}' not found in HTML`);
                }
            }
        } else {
            alert(`${recordType} with ID ${recordId} not found`);
        }
    }

    async createRecord(recordType, recordData) {
        try {
            const response = await fetch(`${this.baseUrl}/api/${recordType}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(recordData),
            });
            if (!response.ok) {
                throw new Error(`Error: ${response.status} - ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Failed to create record:", error);
            return null;
        }
    }

    async updateRecordById(recordType, recordId, updateData) {
        try {
            const response = await fetch(`${this.baseUrl}/api/${recordType}/${recordId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(updateData),
            });
            if (!response.ok) {
                throw new Error(`Error: ${response.status} - ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Failed to update record:", error);
            return null;
        }
    }

    async deleteRecordById(recordType, recordId) {
        try {
            const response = await fetch(`${this.baseUrl}/api/${recordType}/${recordId}`, {
                method: "DELETE",
            });
            if (!response.ok) {
                throw new Error(`Error: ${response.status} - ${response.statusText}`);
            }
            return true;
        } catch (error) {
            console.error("Failed to delete record:", error);
            return false;
        }
    }
}