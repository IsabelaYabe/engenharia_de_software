/**
 * DatabaseManagerClient
 * 
 * Class responsible for performing CRUD (Create, Read, Update, Delete) operations
 * via a RESTful API. This class enables interaction with data stored in a backend
 * and provides that information to a web application.
 * 
 * 
 * Author: Isabela Yabe
 */

class DatabaseManagerClient {
    /**
     * Constructor for the DatabaseManagerClient class.
     * @param {string} baseUrl - The base URL for making API requests.
    */
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    /**
     * Fetches a record by its type and ID through a GET request to the API.
     * @param {string} recordType - The type of the record (e.g., 'product', 'user').
     * @param {number|string} recordId - The ID of the record to be fetched.
     * @returns {Object|null} - Returns the record as a JSON object if found, or null if an error occurs.
     */
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

    /**
     * Loads and populates item details in the HTML interface by fetching data from the API.
     * @param {string} recordType - The type of the record (e.g., 'product').
     * @param {number|string} recordId - The ID of the record to be fetched.
     * @param {Array<string>} itemDetails - Array containing the names of the properties to be used to update the HTML interface (e.g., ['name', 'price']).
     */
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

    /**
     * Creates a new record in the server via a POST request to the API.
     * @param {string} recordType - The type of the record (e.g., 'product', 'user').
     * @param {Object} recordData - The data of the new record to be created.
     * @returns {Object|null} - Returns the newly created record as a JSON object if successful, or null if an error occurs.
     */
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

    /**
     * Updates an existing record by its type and ID via a PUT request to the API.
     * @param {string} recordType - The type of the record (e.g., 'product', 'user').
     * @param {number|string} recordId - The ID of the record to be updated.
     * @param {Object} updateData - The updated data of the record.
     * @returns {Object|null} - Returns the updated record as a JSON object if successful, or null if an error occurs.
     */
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

    /**
     * Deletes a record by its type and ID via a DELETE request to the API.
     * @param {string} recordType - The type of the record (e.g., 'product', 'user').
     * @param {number|string} recordId - The ID of the record to be deleted.
     * @returns {boolean} - Returns true if the deletion was successful, or false if an error occurs.
     */
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