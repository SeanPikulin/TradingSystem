import React, { FC, useState } from 'react';
import {
	Collapse,
	IconButton,
	ListItem,
	ListItemSecondaryAction,
	ListItemText,
} from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';

import { DecisionRule, Discount, isDiscountComplex, isDiscountSimple } from '../../types';
import GenericList from './GenericList';

type DiscountNodeProps = {
	discount: Discount;
	onCreate: (father_id: string) => void;
	onDelete?: (discountId: string) => void;
	productIdToString: (productId: string) => string;
};

const DiscountNode: FC<DiscountNodeProps> = ({
	discount,
	onCreate,
	onDelete,
	productIdToString,
}) => {
	const [open, setOpen] = useState(false);
	const handleClick = () => {
		setOpen(!open);
	};

	function decisionRuleToString(decisionRule: DecisionRule): string {
		const ruleToString: { [key in DecisionRule]: string } = {
			first: 'first discount',
			max: 'best discount value',
			min: 'worst discount value',
		};
		return ruleToString[decisionRule];
	}

	function discountToString(discount: Discount) {
		if (isDiscountSimple(discount)) {
			const discountOn =
				discount.context.obj === 'store'
					? 'all products'
					: discount.context.obj === 'category'
					? `all products in the ${discount.context.id} category`
					: `product "${productIdToString(discount.context.id)}"`;
			return `${discount.percentage}% discount on ${discountOn}`;
		} else {
			return `${discount.type.toUpperCase()}${
				discount.type === 'xor'
					? ` - decision rule: ${decisionRuleToString(discount.decision_rule)}`
					: ''
			}`;
		}
	}

	return (
		<>
			<ListItem button onClick={handleClick}>
				{isDiscountComplex(discount) && (
					<IconButton edge="start" aria-label="delete">
						{open ? <ExpandLess /> : <ExpandMore />}
					</IconButton>
				)}
				<ListItemText primary={discountToString(discount)} />
				{onDelete && (
					<ListItemSecondaryAction onClick={() => onDelete(discount.id)}>
						<IconButton edge="end" aria-label="delete">
							<DeleteForeverOutlinedIcon />
						</IconButton>
					</ListItemSecondaryAction>
				)}
			</ListItem>
			{isDiscountComplex(discount) && (
				<Collapse in={open} timeout="auto">
					<GenericList
						data={discount.discounts}
						onCreate={() => onCreate(discount.id)}
						createTxt="+ Add new discount"
						padRight
					>
						{(discount) => (
							<DiscountNode
								key={discount.id}
								discount={discount}
								onCreate={onCreate}
								onDelete={onDelete}
								productIdToString={productIdToString}
							/>
						)}
					</GenericList>
				</Collapse>
			)}
		</>
	);
};

export default DiscountNode;
