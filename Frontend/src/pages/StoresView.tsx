import React, { FC, useEffect, useState, useRef } from 'react';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import '../styles/StoresView.scss';
import ProductSearch from '../components/ProductSearch';
import storesToProducts from '../components/storesProductsMap';
import useAPI from '../hooks/useAPI';
import { Product, Store, ProductQuantity } from '../types';

type StoresViewProps = {
	propsAddProduct: (product: Product, storeID: string) => void;
	location: any;
};

const StoresView: FC<StoresViewProps> = ({ propsAddProduct, location }: StoresViewProps) => {
	const [presentProducts, setProducts] = useState<ProductQuantity[]>([]);
	const [stores, setStores] = useState<Store[]>([]);

	// storeID
	const [storeID, setStoreID] = useState<string>(
		location.state !== undefined ? location.state.storeID : ''
	);
	const storeName = useRef<string>('');
	const productsObj = useAPI<Product[]>('/get_products_by_store');
	useEffect(() => {
		const getQuantityOfProduct = (productID: string, storeID: string) => {
			for (var i = 0; i < stores.length; i++) {
				if (stores[i].id === storeID) {
					for (var j = 0; j < Object.keys(stores[i].ids_to_quantities).length; j++) {
						if (Object.keys(stores[i].ids_to_quantities)[j] === productID) {
							return Object.values(stores[i].ids_to_quantities)[j];
						}
					}
				}
			}
			return 0;
		};
		const gerStoreNameByID = (storeID: string) => {
			for (var i = 0; i < stores.length; i++) {
				if (stores[i].id === storeID) {
					return stores[i].name;
				}
			}
			return '';
		};

		storeName.current = gerStoreNameByID(storeID);
		if (storeName.current !== '') {
			productsObj.request({ store_id: storeID }).then(({ data, error, errorMsg }) => {
				if (!error && data !== null) {
					let productsArray: Product[] = data.data;
					let productQuantityArr: ProductQuantity[] = productsArray.map((product) => {
						return {
							id: product.id,
							name: product.name,
							category: product.category,
							price: product.price,
							keywords: product.keywords,
							quantity: getQuantityOfProduct(product.id, storeID),
						};
					});
					setProducts(productQuantityArr);
				} else {
					// alert(errorMsg);
				}
			});
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [storeID]);

	const storesObj = useAPI<Store[]>('/get_stores_details');
	useEffect(() => {
		storesObj.request().then(({ data, error, errorMsg }) => {
			if (!error && data !== null) {
				setStores(data.data);
			} else {
				// alert(errorMsg);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const handleChange = (e: any) => {
		setStoreID(e.target.value);
		//   set store causes use effect and rendering new products
	};
	const matrix_length = 3;
	const setProductsInMatrix = () => {
		var matrix = [];
		for (var i = 0; i < Math.ceil(presentProducts.length / 3); i++) {
			matrix[i] = new Array(matrix_length);
		}
		for (i = 0; i < matrix.length; i++) {
			for (var j = 0; j < matrix[i].length; j++) {
				matrix[i][j] = presentProducts[matrix[i].length * i + j];
			}
		}
		return matrix;
	};
	return (
		<div className="StoresDiv">
			<FormControl
				style={{ marginLeft: '5%', width: '100%', fontSize: 'large', height: '94%' }}
			>
				<h3>Choose Store</h3>
				<Select
					value={storeID}
					style={{ fontSize: '2rem', width: '50%' }}
					onChange={(e) => handleChange(e)}
				>
					{stores.map((store) => {
						return (
							<MenuItem
								value={store.id}
								key={Object.keys(storesToProducts).indexOf(store.name)}
							>
								{store.name}
							</MenuItem>
						);
					})}
				</Select>
				<div className="productCards">
					{storeName.current !== '' ? (
						setProductsInMatrix().map((row, i) => {
							return (
								<div className="cardsRow">
									{row.map((cell, j) => {
										return (
											<ProductSearch
												key={i * matrix_length + j}
												storeID={storeID}
												content={cell !== undefined ? cell.name : ''}
												price={cell !== undefined ? cell.price : 0}
												quantity={cell !== undefined ? cell.quantity : 0}
												category={cell !== undefined ? cell.category : ''}
												clickAddProduct={() =>
													propsAddProduct(cell, storeID)
												}
											></ProductSearch>
										);
									})}
								</div>
							);
						})
					) : (
						<div className="placeHolder"></div>
					)}
				</div>
			</FormControl>
		</div>
	);
};

export default StoresView;
