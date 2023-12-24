import React, { useState, useEffect } from 'react'
import Modal from 'react-modal';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [salespersons, setSalespersons] = useState([]);
  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [sales, setSales] = useState([]);
  const [quarterlyCommission, setQuarterlyCommission] = useState([]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingEntity, setEditingEntity] = useState(null);
  const [editingEntityType, setEditingEntityType] = useState('');

  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const [newSale, setNewSale] = useState({
    product_id: '',
    salesperson_id: '',
    customer_id: '',
    sales_date: '',
  });

  const [quarter, setQuarter] = useState('');

  
  async function fetchData(endpoint) {
    try {
      const response = await fetch(`http://localhost:5000/${endpoint}`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      return null;
    }
  }
  
  const fetchEntities = async () => {
    const salespersonsData = await fetchData('salespersons');
    const productsData = await fetchData('products');
    const customersData = await fetchData('customers');
    const salesData = await fetchData(`sales?start_date=${startDate}&end_date=${endDate}`);
    const quarterlyCommissionData = await fetchData(`quarterly-commissions?quarter=${quarter}`);

    if (customersData) setCustomers(customersData.customers);
    if (productsData) setProducts(productsData.products);
    if (salesData) setSales(salesData.sales);
    if (salespersonsData) setSalespersons(salespersonsData.salespersons);
    if (quarterlyCommissionData) setQuarterlyCommission(quarterlyCommissionData.quarterly_commission);
  };

  useEffect(() => {
    fetchEntities();
  }, [quarter, startDate, endDate])


  const handleDataUpdates = async () => {
    try {
      const response = await fetch(`http://localhost:5000/update-${editingEntityType}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editingEntity),
      });
  
      if (response.ok) {
        fetchEntities();
        closeEditModal();
      } else {
        console.error('Failed to update entity');
      }
    } catch (error) {
      console.error('Error updating entity:', error);
    }
  };
  
  const handleCreateSale = async () => {
    try {
      const response = await fetch('http://localhost:5000/create-sale', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSale),
      });
  
      if (response.ok) {
        setNewSale({
          product_id: '',
          salesperson_id: '',
          customer_id: '',
          sales_date: '',
        });
        fetchEntities();
      } else {
        console.error('Failed to create sale');
      }
    } catch (error) {
      console.error('Error creating sale:', error);
    }
  };



  const openEditModal = (entity, entityType) => {
    setEditingEntity(entity);
    setEditingEntityType(entityType);
    setIsModalOpen(true);
  };

  const closeEditModal = () => {
    setEditingEntity(null);
    setEditingEntityType('');
    setIsModalOpen(false);
  };

  const handleInputChange = (fieldName, value) => {
    setEditingEntity((prevEntity) => ({
      ...prevEntity,
      [fieldName]: value,
    }));
  };

  const renderEdit = () => {
    if (editingEntityType === '') {
      return (
        <>
        </>
      )
    } else if (editingEntityType === 'product') {
      return (
        <>
        <h2>Edit Product</h2>
          <ul>
            <li>
              <label>Name </label>
              <input
                type="text"
                name="name"
                value={editingEntity.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
              />
            </li>
            <li>
              <label>Manufacturer </label>
              <input
                type="text"
                name="manufacturer"
                value={editingEntity.manufacturer}
                onChange={(e) => handleInputChange('manufacturer', e.target.value)}
              />
            </li>
            <li>
              <label>Style </label>
              <input
                type="text"
                name="style"
                value={editingEntity.style}
                onChange={(e) => handleInputChange('style', e.target.value)}
              />
            </li>
            <li>
              <label>Purchase Price ($) </label>
              <input
                type="text"
                name="purchase_price"
                value={editingEntity.purchase_price}
                onChange={(e) => handleInputChange('purchase_price', e.target.value)}
              />
            </li>
            <li>
              <label>Sale Price ($) </label>
              <input
                type="text"
                name="sale_price"
                value={editingEntity.sale_price}
                onChange={(e) => handleInputChange('sale_price', e.target.value)}
              />
            </li>
            <li>
              <label>Qty On Hand </label>
              <input
                type="text"
                name="qty_on_hand"
                value={editingEntity.qty_on_hand}
                onChange={(e) => handleInputChange('qty_on_hand', e.target.value)}
              />
            </li>
            <li>
              <label>Commission Percentage </label>
              <input
                type="text"
                name="commission_percentage"
                value={editingEntity.commission_percentage}
                onChange={(e) => handleInputChange('commission_percentage', e.target.value)}
              />
            </li>
          </ul>
        </>
      )
    } else {
      return (
        <>
        <h2>Edit Salesperson</h2>
          <ul>
            <li>
              <label>First Name </label>
              <input
                type="text"
                name="first_name"
                value={editingEntity.first_name}
                onChange={(e) => handleInputChange('first_name', e.target.value)}
              />
            </li>
            <li>
              <label>Last Name </label>
              <input
                type="text"
                name="last_name"
                value={editingEntity.last_name}
                onChange={(e) => handleInputChange('last_name', e.target.value)}
              />
            </li>
            <li>
              <label>Address </label>
              <input
                type="text"
                name="address"
                value={editingEntity.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
              />
            </li>
            <li>
              <label>Phone </label>
              <input
                type="text"
                name="phone"
                value={editingEntity.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
              />
            </li>
            <li>
              <label>Start Date </label>
              <input
                type="text"
                name="start_date"
                value={editingEntity.start_date}
                onChange={(e) => handleInputChange('start_date', e.target.value)}
              />
            </li>
            <li>
              <label>Termination Date </label>
              <input
                type="text"
                name="termination_date"
                value={editingEntity.termination_date}
                onChange={(e) => handleInputChange('termination_date', e.target.value)}
              />
            </li>
            <li>
              <label>Manager </label>
              <input
                type="text"
                name="manager"
                value={editingEntity.manager}
                onChange={(e) => handleInputChange('manager', e.target.value)}
              />
            </li>
          </ul>
        </>
      )
    }
  }


  Modal.setAppElement('#root');

  return (
    <div className="container">
      <div className="container bg-primary text-white p-3">
        <h1 className="mb-4">BeSpoked Bikes</h1>
      </div>


      <div className="row">
        <div className="col">
          <h2>Salespersons</h2>
          <ul className="list-group">
            {Object.values(salespersons).map(salesperson => (
              <li key={`SP${salesperson.id}`} className="list-group-item">
                <strong><p className="mb-3">{`${salesperson.first_name} ${salesperson.last_name}`}</p></strong>
                <p className="mb-1">Address: {salesperson.address}</p>
                <p className="mb-1">Phone: {salesperson.phone}</p>
                <p className="mb-1">Start Date: {salesperson.start_date}</p>
                <p className="mb-1">Termination Date: {salesperson.termination_date}</p>
                <p className="mb-1">Manager: {salesperson.manager}</p>
                <button className="btn btn-primary" onClick={() => openEditModal(salesperson, 'salesperson')}>Edit</button>
              </li>
            ))}
          </ul>
        </div>


        <div className="col">
          <h2>Products</h2>
          <ul className="list-group">
          {Object.values(products).map(product => (
            <li key={`P${product.id}`} className="list-group-item">
              <strong><p className="mb-3">{product.name}</p></strong>
              <p className="mb-1">Manufacturer: {product.manufacturer}</p>
              <p className="mb-1">Style: {product.style}</p>
              <p className="mb-1">Purchase Price: ${product.purchase_price}</p>
              <p className="mb-1">Sale Price: ${product.sale_price}</p>
              <p className="mb-1">Qty-On-Hand: {product.qty_on_hand}</p>
              <p className="mb-1">Commission Percentage: {product.commission_percentage*100}%</p>
              <button className="btn btn-primary" onClick={() => openEditModal(product, 'product')}>Edit</button>
            </li>
          ))}
          </ul>
        </div>


      <Modal
        isOpen={isModalOpen}
        onRequestClose={closeEditModal}
        contentLabel="Edit Product Modal"
      >
        {renderEdit()}
        <button className="btn btn-primary" onClick={handleDataUpdates}>Save Changes</button>
        <button className="btn btn-secondary" onClick={closeEditModal}>Cancel</button>
      </Modal>


        <div className="col">
          <h2>Customers</h2>
          <ul className="list-group">
          {Object.values(customers).map(customer => (
            <li key={`C${customer.id}`} className="list-group-item">
              <strong><p className="mb-3">{`${customer.first_name} ${customer.last_name}`}</p></strong>
              <p className="mb-1">Address: {customer.address}</p>
              <p className="mb-1">Phone: {customer.phone}</p>
              <p className="mb-1">Start Date: {customer.start_date}</p>
            </li>
          ))}
          </ul>
        </div>
      </div>


      <div className="container mt-5">
        <h2 className="mb-3">Create a Sale</h2>
        <form>
          <div className="mb-3">
            <label htmlFor="productSelect" className="form-label">Product</label>
            <select
              id="productSelect"
              className="form-select"
              name="product_id"
              value={newSale.product_id}
              onChange={(e) => setNewSale({ ...newSale, product_id: e.target.value })}
            >
              <option value="">Select a Product</option>
              {Object.values(products).map(product => (
                <option key={product.id} value={product.id}>{product.name}</option>
              ))}
            </select>
          </div>

          <div className="mb-3">
            <label htmlFor="salespersonSelect" className="form-label">Salesperson</label>
            <select
              id="salespersonSelect"
              className="form-select"
              name="salesperson_id"
              value={newSale.salesperson_id}
              onChange={(e) => setNewSale({ ...newSale, salesperson_id: e.target.value })}
            >
              <option value="">Select a Salesperson</option>
              {Object.values(salespersons)
                .filter(salesperson => (
                  salesperson.termination_date === '' || new Date(salesperson.termination_date).toISOString().split('T')[0] > new Date().toISOString().split('T')[0]
                ))
                .map(salesperson => (
                  <option key={salesperson.id} value={salesperson.id}>
                    {`${salesperson.first_name} ${salesperson.last_name}`}
                  </option>
                ))}
            </select>
          </div>

          <div className="mb-3">
            <label htmlFor="customerSelect" className="form-label">Customer</label>
            <select
              id="customerSelect"
              className="form-select"
              name="customer_id"
              value={newSale.customer_id}
              onChange={(e) => setNewSale({ ...newSale, customer_id: e.target.value })}
            >
              <option value="">Select a Customer</option>
              {Object.values(customers).map(customer => (
                <option key={customer.id} value={customer.id}>
                  {`${customer.first_name} ${customer.last_name}`}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-3">
            <label htmlFor="salesDateInput" className="form-label">Sales Date</label>
            <input
              type="date"
              id="salesDateInput"
              className="form-control"
              name="sales_date"
              value={newSale.sales_date}
              onChange={(e) => setNewSale({ ...newSale, sales_date: e.target.value })}
            />
          </div>
          <button type="button" className="btn btn-primary" onClick={handleCreateSale}>Create Sale</button>
        </form>
      </div>


      <div className="row mt-5">
        <div className="col">
          <h2>Sales</h2>
          <div className="row mb-3">
            <div className="col-md-3">
              <input
                type="date"
                id="startDate"
                className="form-control"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>

            <div className="col-md-3">
              <input
                type="date"
                id="endDate"
                className="form-control"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </div>

          <ul className="list-group">
            {Object.values(sales).map(sale => (
              <li key={`S${sale.id}`} className="list-group-item">
                <p className="mb-1">Product: {sale.product}</p>
                <p className="mb-1">Customer: {sale.customer}</p>
                <p className="mb-1">Sales Date: {sale.sales_date}</p>
                <p className="mb-1">Price: ${sale.sale_price}</p>
                <p className="mb-1">Salesperson: {sale.salesperson}</p>
                <p className="mb-1">Salesperson Commission: {sale.commission_percentage * 100}%</p>
              </li>
            ))}
          </ul>
        </div>


        <div className="col">
          <h2>Quarterly Salesperson Commission Report</h2>
          <div className="btn-group mb-3" role="group" aria-label="Quarterly Selection">
            <input type="radio" className="btn-check" name="quarter" id="q1" autoComplete="off" onClick={() => setQuarter('Q1')} />
            <label className="btn btn-outline-primary" htmlFor="q1">Q1</label>

            <input type="radio" className="btn-check" name="quarter" id="q2" autoComplete="off" onClick={() => setQuarter('Q2')} />
            <label className="btn btn-outline-primary" htmlFor="q2">Q2</label>

            <input type="radio" className="btn-check" name="quarter" id="q3" autoComplete="off" onClick={() => setQuarter('Q3')} />
            <label className="btn btn-outline-primary" htmlFor="q3">Q3</label>

            <input type="radio" className="btn-check" name="quarter" id="q4" autoComplete="off" onClick={() => setQuarter('Q4')} />
            <label className="btn btn-outline-primary" htmlFor="q4">Q4</label>
          </div>
          <ul className="list-group">
            {Object.entries(quarterlyCommission).map(([salespersonId, commissionInfo]) => (
              <li key={salespersonId} className="list-group-item">
                <h5 className="mb-1">{commissionInfo.salesperson}</h5>
                <p className="mb-1">Total Sales: ${commissionInfo.total_sales}</p>
                <p className="mb-1">Total Commission: ${commissionInfo.total_commission}</p>
              </li>
            ))}
          </ul>
        </div>

      </div>

    </div>
  );
}

export default App;
